# aws-tutorials
# Flask SQS Message Processor 📬

This application is designed to interact with AWS services, specifically SQS and SSM, to manage messages and API keys.
It was originally setup on EC2 via SSH.

## Features ✨

- **Retrieve API Key**: Securely fetch API keys from AWS SSM Parameter Store.
- **SQS Message Handling**: Poll and delete messages from an SQS queue.
- **Web Interface**: Render a simple web page to display messages.
- **API Integration**: Post messages to an external API endpoint.

## Installation 📦

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Environment Setup**: Ensure you have Python and pip installed.
3. **Install Dependencies**: Run `pip install -r requirements.txt` to install necessary packages.
4. **Environment Variables**: Create a `.env` file with the following variables:
   - `SQS_QUEUE_URL`
   - `AWS_REGION`
   - `API_ENDPOINT`
   - `SSM_PARAMETER_NAME`

## Usage 🚀

- **Run the Application**: Execute the script using `python app.py`.
- **Access the Web Interface**: Open your browser and navigate to `https://localhost:5000/`.
- **Interact with SQS**: Use the web interface to view and manage SQS messages.

## Endpoints 🔗

- `/:` Main page rendering.
- `/get_sqs_messages`: Fetches and deletes messages from the SQS queue.
- `/create_message`: Accepts a message from the client and posts it to the specified API.

## Security 🔒

- **SSL**: The application runs over HTTPS using SSL certificates (`cert.pem` and `key.pem`).

## Requirements 🛠️

- Python 3.x
- Flask
- Boto3
- Requests
- Python-dotenv

## License 📄

This project is licensed under the MIT License. Feel free to use and modify it as needed.

Enjoy managing your SQS messages with Flask! 😊