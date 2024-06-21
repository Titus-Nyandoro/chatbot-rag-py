# VUA Chatbot

## Overview
The VUA Chatbot project integrates OpenAI's embeddings with LangChain to create a document-based chatbot. Users interact with the chatbot primarily via SMS, receiving responses based on document data. The project handles document loading, chunking, storage in a Chroma vector store, and provides a chat interface through a Flask web application.

## Table of Contents
- [Getting Started](#getting-started)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
- [Creating the Database](#creating-the-database)
- [Running the Application](#running-the-application)
- [Integration with Africa's Talking](#integration-with-africas-talking)
- [Africa's Talking: Sandbox vs. Production](#africas-talking-sandbox-vs-production)
- [JSON Format Guide](#json-format-guide)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Virtual environment (optional but recommended)

### Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/Titus-Nyandoro/chatbot-rag-py.git
   cd chatbot-rag-py
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**
   ```sh
   pip install -r requirements.txt
   pip install "unstructured[pdf]"
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root directory and add your OpenAI and Africa's Talking API keys:
   ```env
   FLASK_SECRET_KEY=optional-secret
   DATABASE_URL=sqlite:///vua.db
   OPENAI_API_KEY=your_openai_api_key
   AT_USERNAME=sandbox
   AT_API_KEY=your_africastalking_api_key
   ```

### Creating the Database
1. **Ensure your documents are in the `data/documents` directory**.
   Place any PDF files you want to include in the database in this directory.

2. **Run the `create_database.py` script**
   ```sh
   python create_database.py
   ```
   This script processes the documents, splits them into chunks, and saves these chunks to the Chroma vector store.

### Running the Application
1. **Run the Flask application**
   ```sh
   python vua_app.py
   ```

2. **Access the application**
   Open your web browser and navigate to `http://127.0.0.1:5000/` to interact with the chatbot.

## Directory Structure
```
vua-chatbot/
├── chroma/                     # Directory for Chroma vector database
├── data/                       # Directory for data files
│   ├── books/                  # Example book files
│   │   └── alice_in_wonderland.txt
│   └── documents/              # Directory for documents to be processed
├── instance/                   # Directory for main scripts
│   ├── compare_embeddings.py   # Script for comparing embeddings
│   ├── create_database.py      # Script for creating the Chroma vector database
│   ├── vua_app.py              # Main application script
│   ├── vua_app_vii.py          # Alternate application script (details needed)
│   └── vua_console_chat.py     # Console chat application script
├── templates/                  # Directory for HTML templates
│   └── index.html              # Main user interface template
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (not included, must be created)
```

## Configuration

### OpenAI Configuration
- Register for an API key at [OpenAI](https://beta.openai.com/signup/).
- Set the OpenAI API key in the `.env` file.

### Africa's Talking Configuration
- Register at [Africastalking](https://account.africastalking.com/) to obtain your username and API key.
- Set your Africastalking username and API key in the `.env` file.

### Flask Configuration
- Set the Flask secret key in the `.env` file.

## Integration with Africa's Talking

### Step 1: Set Up Africa's Talking Account

1. **Sign Up and Create an Application**
   - Go to [Africastalking](https://account.africastalking.com/auth/register).
   - Sign up for an account or log in if you already have one.
   - Navigate to the "Sandbox Apps" section and create a new application. This will generate a `USERNAME` and an `API KEY` for the sandbox environment.

2. **Add SMS Service**
   - Go to your application dashboard.
   - Click on "SMS" under the Services section.
   - Enable the SMS service for your application.

3. **Get API Credentials**
   - Navigate to the "API Key" section on your dashboard.
   - Copy the `USERNAME` (usually "sandbox" for testing) and `API KEY`.

### Step 2: Install Africa's Talking Python SDK

Add Africa's Talking SDK to your project:
```sh
pip install africastalking
```

### Step 3: Configure Your Application

1. **Update Environment Variables**
   - Open the `.env` file in your project root directory.
   - Add your Africa's Talking credentials:
     ```env
     AT_USERNAME=sandbox
     AT_API_KEY=your_africastalking_api_key
     ```

2. **Modify Your Code to Send SMS**
   - Create a new file `send_sms.py` or add the following code to an existing script:
     ```python
     import africastalking

     # Set your app credentials
     username = "sandbox"  # Use 'sandbox' for testing
     api_key = "your_africastalking_api_key"  # Replace with your actual API key

     # Initialize the SDK
     africastalking.initialize(username, api_key)

     # Get the SMS service
     sms = africastalking.SMS

     def send_sms(message, recipients):
         try:
             response = sms.send(message, recipients)
             print(response)
         except Exception as e:
             print(f"Encountered an error while sending SMS: {e}")

     if __name__ == "__main__":
         message = "Hello from VUA Chatbot!"
         recipients = ["+254712345678"]  # Replace with your phone number
         send_sms(message, recipients)
     ```

### Step 4: Integrate with Chatbot

1. **Update Chatbot Code to Use SMS Service**
   - Modify `vua_app.py` to integrate the SMS sending functionality:
     ```python
     import os
     from flask import Flask, request, jsonify
     from send_sms import send_sms  # Import your send_sms function

     app = Flask(__name__)
     app.secret_key = os.getenv('FLASK_SECRET_KEY')

     @app.route('/sms', methods=['POST'])
     def sms_reply():
         data = request.get_json()
         message = data.get('message')
         phone_number = data.get('phone_number')

         # Your chatbot processing logic here
         bot_reply = "This is a response from VUA Chatbot."

         # Send SMS reply
         send_sms(bot_reply, [phone_number])

         return jsonify({"reply": bot_reply})

     if __name__ == "__main__":
         app.run(debug=True)
     ```

### Step 5: Test SMS Integration
- Run your Flask application:
  ```sh
  python vua_app.py
  ```
- Use a tool like Postman or curl to send a POST request to `http://127.0.0.1:5000/sms` with the following JSON payload:
  ```json
  {
    "message": "Hello, Chatbot!",
    "phone_number": "+254712345678"
  }
  ```
- Check if the SMS is sent to the specified phone number.

## Africa's Talking: Sandbox vs. Production

### Sandbox Environment

1. **Purpose**
   - The sandbox environment is used for development and testing.
   - It allows developers to simulate SMS sending without incurring costs or sending messages to actual phone numbers.

2. **Limitations**
   - SMS messages in the sandbox can only be sent to specific test numbers (e.g., `+254712345678`).
   - Actual phone numbers will not receive the messages.
   - Costs are simulated, and no real charges apply.

3. **Configuration**
   - Ensure you use `sandbox` as the `USERNAME` and the corresponding `API KEY` for the sandbox.
   - Test messages appear in the Africa's Talking sandbox dashboard.

### Production Environment

1. **Purpose**
   - The production environment is used for live applications.
   - SMS messages are sent to actual phone numbers, and real charges apply.

2. **Requirements**
   - You must apply for and obtain production credentials from Africa's Talking.
   - Go to the [Africa's Talking dashboard](https://account.africastalking.com) and request production access for your application.

3. **Configuration**
   - Replace `sandbox` with your production `USERNAME` and use the production `API KEY`.
   - Messages sent from production credentials will be delivered to real phone numbers.

4. **Considerations**
   - Ensure you comply with the local regulations and guidelines for sending SMS messages in your target region.
   - Monitor your usage and costs via the Africa's Talking dashboard.

### Switching from Sandbox to Production

1. **Change Credentials**
   - Update your `.env` file with production credentials:


     ```env
     AT_USERNAME=your_production_username
     AT_API_KEY=your_production_api_key
     ```

2. **Test Thoroughly**
   - Perform extensive testing in the sandbox environment before switching to production.
   - Once ready, switch to production and test with a small, controlled number of real recipients to verify functionality.

### SMS Delivery to Different Telcos

1. **Supported Telcos**
   - Africa's Talking supports SMS delivery to multiple telecom operators in various countries.
   - Some of the major telecom operators include:
     - **Kenya**: Safaricom, Airtel, Telkom Kenya
     - **Uganda**: MTN Uganda, Airtel Uganda
     - **Nigeria**: MTN Nigeria, Glo Mobile, Airtel Nigeria
     - **Tanzania**: Vodacom Tanzania, Tigo Tanzania, Airtel Tanzania

2. **Delivery Considerations**
   - Ensure the recipients’ phone numbers are in the correct international format (e.g., `+254` for Kenya).
   - Check for any specific requirements or restrictions for SMS delivery with each telecom operator.
   - Some telcos may have specific message length limits or formatting rules.

3. **Monitoring and Reporting**
   - Use the Africa's Talking dashboard to monitor SMS delivery reports and track costs.
   - Analyze the delivery reports to ensure messages are successfully reaching the intended recipients across different telecom networks.

## JSON Format Guide

### Chat Request Format
```json
{
  "message": "Your message here",
  "phone_number": "Your phone number here"
}
```

### Chat Response Format
```json
{
  "reply": "Bot's reply to the user message"
}
```

### SMS Request Format
```json
{
  "to": "+254712345678",
  "message": "Your SMS message here"
}
```

### SMS Response Format
```json
{
  "SMSMessageData": {
    "Message": "Sent to 1/1 Total Cost: 0.8000",
    "Recipients": [
      {
        "statusCode": 101,
        "number": "+254712345678",
        "status": "Success",
        "cost": "KES 0.8000",
        "messageId": "ATXid_ba89924c2d344f36b16e123fefefefef"
      }
    ]
  }
}
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request or report issues.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
