# Flask SQS & SSM Tutorial Application 📬☁️

This is a sample Flask application demonstrating interaction with AWS SQS (Simple Queue Service) and AWS SSM (Systems Manager) Parameter Store. It was developed as part of a tutorial, potentially run on an EC2 instance via SSH, but can be adapted for other environments.

![Project description](https://github.com/PlayfulDevBit/aws-tutorials/blob/main/templates/static/img.jpg)

> **⚠️ Important Security Notice:** This code is intended for **educational purposes**. Before using or deploying it, please review the following:
>
> 1.  **Sensitive Files:** **NEVER** commit sensitive files like your AWS credentials, `.env` files containing secrets, or SSL private keys (`.pem` files) to Git or any public repository. Ensure these are listed in your `.gitignore` file.
> 2.  **`.env` File:** This project uses a `.env` file to load configuration. This file should contain your specific AWS resource names and potentially other configuration. **Do not commit this file.** A template (`.env.example`) should be provided.
> 3.  **SSL Certificates:** The code includes setup for HTTPS using `cert.pem` and `key.pem`. These are typically generated for local development. **Do not commit your private key (`key.pem`).** For production, use proper certificate management.
> 4.  **Flask Debug Mode:** The application might run with `debug=True` in `app.py` for development convenience. **This is highly insecure for production environments** as it can expose sensitive information and allow arbitrary code execution. Ensure debug mode is turned OFF (`debug=False` or removed) before any deployment.

## Features ✨

*   **Secure API Key Retrieval**: Fetches an API key securely from AWS SSM Parameter Store (using `WithDecryption=True`).
*   **SQS Message Polling**: Polls messages from a specified SQS queue.
*   **SQS Message Deletion**: Deletes messages from the queue after successful processing.
*   **Simple Web Interface**: Renders a basic web page using Flask to display retrieved messages.
*   **API Interaction**: Sends processed messages to an external API endpoint using the retrieved API key.

## Prerequisites 🛠️

*   Python 3.x
*   Pip (Python package installer)
*   An AWS Account
*   AWS CLI installed and configured (recommended for easier credential setup) or environment variables set for Boto3.
*   Git

## Setup Instructions ⚙️

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On macOS/Linux
    source venv/bin/activate
    # On Windows
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure AWS Credentials:**
    Ensure your environment is configured so that `boto3` can find AWS credentials. Common methods include:
    *   AWS credentials file (`~/.aws/credentials`)
    *   Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)
    *   IAM Role attached to the compute environment (e.g., EC2 instance profile) - **Recommended for AWS deployments**.
    *   Refer to the [Boto3 Credentials Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) for details. **Do not hardcode credentials in your code.**

5.  **Set up AWS Resources:**
    *   **SQS Queue:** Create an SQS Standard Queue in your desired AWS region. Note down its **Queue URL**.
    *   **SSM Parameter:** Create a Parameter in AWS Systems Manager Parameter Store.
        *   Use type `SecureString`. AWS KMS will encrypt it.
        *   Store your external API key as the value.
        *   Note down the exact **Parameter Name**.

6.  **Create `.env` File:**
    Create a file named `.env` in the project root. **Do not commit this file to Git.** Add the following variables, replacing the placeholder values with your actual resource details:
    ```dotenv
    # .env file
    SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789012/MyQueueName
    AWS_REGION=us-east-1
    API_ENDPOINT=https://api.example.com/messages
    SSM_PARAMETER_NAME=/myapp/prod/api_key
    # Optional: To disable Flask debug mode safely
    # FLASK_DEBUG=False
    ```
    *(Consider creating a `.env.example` file with placeholder values to commit, guiding users on what's needed).*

7.  **Generate Local SSL Certificates (for Development):**
    The application is configured to run over HTTPS (`https://`). For local development, you can generate self-signed certificates. **Do not commit the private key (`key.pem`).**
    Using OpenSSL:
    ```bash
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 \
      -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"
    ```
    *(Note: Browsers will show a warning for self-signed certificates).*

8.  **Configure `.gitignore`:**
    Ensure you have a `.gitignore` file in your project root to prevent committing sensitive information and unnecessary files. It should include at least:
    ```gitignore
    # Environment variables
    .env
    *.env.*
    !.env.example

    # SSL Certificates and Keys (especially private key)
    *.pem

    # Python specific
    __pycache__/
    *.py[cod]
    *$py.class
    venv/
    .venv/
    env/

    # Build artifacts
    dist/
    build/
    *.egg-info/
    ```

## Running the Application 🚀

1.  **Activate Virtual Environment:** (If not already active)
    ```bash
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

2.  **Run the Flask Development Server:**
    ```bash
    python app.py
    ```
    *   Access the application at `https://localhost:5000/` (or `https://0.0.0.0:5000/`). You'll likely need to accept the browser warning for the self-signed certificate.
    *   **Warning:** This uses the Flask development server with `debug=True` (unless changed). **Do not use this setup for production.**

## Endpoints 🔗

*   `GET /`: Renders the main HTML page, initially showing no messages.
*   `GET /get_sqs_messages`: An endpoint to poll, delete, and retrieve new messages from the SQS queue. Returns JSON data.
*   `POST /create_message`: An endpoint that accepts form data (`message_text`) and posts it to the configured `API_ENDPOINT` using the API key fetched from SSM.

## Requirements (from `requirements.txt`) 🛠️

*   Flask
*   Boto3
*   Requests
*   python-dotenv

