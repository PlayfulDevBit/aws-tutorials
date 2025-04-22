from flask import Flask, render_template, jsonify, request
import boto3
import datetime
import ssl
import os
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get environment variables
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_REGION = os.getenv("AWS_REGION")
API_ENDPOINT = os.getenv("API_ENDPOINT")
SSM_PARAMETER_NAME = os.getenv("SSM_PARAMETER_NAME")

# Initialize SSM client (outside the function for reuse)
ssm_client = boto3.client('ssm', region_name=AWS_REGION)

def get_api_key_from_ssm():
    """Retrieves the API key from SSM Parameter Store."""
    try:
        response = ssm_client.get_parameter(
            Name=SSM_PARAMETER_NAME,
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Error retrieving API key from SSM: {e}")
        return None


def poll_and_delete_messages():
    """Polls and deletes messages from the SQS queue.
    Returns a list of message data (body and timestamp)."""

    sqs = boto3.client('sqs', region_name=AWS_REGION)
    message_data = []

    try:
        while True:
            response = sqs.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10
            )

            messages = response.get('Messages', [])

            if not messages:
                break

            for message in messages:
                message_body = message['Body']
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                receipt_handle = message['ReceiptHandle']

                message_data.append({"body": message_body, "timestamp": timestamp})

                # Delete the message from the queue
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=receipt_handle
                )

    except Exception as e:
        print(f"Error polling and deleting messages: {e}")  # Log the error for debugging
        return None  # Or raise the exception if you want it to propagate

    return message_data


@app.route("/")
def index():
    """Renders the main page."""
    return render_template("index.html", messages=[])


@app.route("/get_sqs_messages")
def get_sqs_messages():
    """Polls SQS for new messages and returns them as JSON."""
    message_data = poll_and_delete_messages()

    if message_data is None:
        return jsonify({"error": "Failed to retrieve messages."}), 500  # Return an error response

    return jsonify(messages=message_data)

@app.route("/create_message", methods=['POST'])
def create_message():
    """Receives a message from the client and posts it to the API."""
    message_text = request.form.get('message_text')  # Get the message from the form

    if not message_text:
        return jsonify({"success": False, "message": "Message text is required."}), 400

    payload = {"body": f'{{"message": "{message_text}", "user": "flask_app"}}'}

    try:
        import requests  # Import requests inside the try block

        api_key = get_api_key_from_ssm()  # Retrieve the API key from SSM
        if not api_key:
            return jsonify({"success": False, "message": "Failed to retrieve API key."}), 500

        headers = {"X-APIkey": api_key, "Content-Type": "application/json"}
        response = requests.post(API_ENDPOINT, headers=headers, json=payload) # Send JSON data

        if response.status_code == 200:
            return jsonify({"success": True, "message": "Message created successfully."})
        else:
            print(f"API Error: Status Code {response.status_code}, Response: {response.text}")
            return jsonify({"success": False, "message": f"API Error: {response.status_code} - {response.text}"}), 500

    except Exception as e:
        print(f"Error posting to API: {e}")
        return jsonify({"success": False, "message": f"Error posting to API: {str(e)}"}), 500


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(debug=True, host='0.0.0.0', ssl_context=context)