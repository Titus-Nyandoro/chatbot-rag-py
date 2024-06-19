# VUA Chatbot

## Overview
The VUA Chatbot project leverages the LangChain library to create a document-based chatbot that utilizes OpenAI's embeddings. The chatbot interacts with users primarily via SMS, providing responses based on document data. The project includes functionality for loading documents, splitting them into manageable chunks, storing these chunks in a Chroma vector store, and providing a chat interface through a Flask web application.

## Table of Contents
- [Getting Started](#getting-started)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
- [Creating the Database](#creating-the-database)
- [Running the Application](#running-the-application)
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
   git clone https://github.com/your-repo/vua-chatbot.git
   cd vua-chatbot
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
   The script currently processes only PDF files. Place any PDF files you want to include in the database in this directory.

2. **Run the `create_database.py` script**
   ```sh
   python create_database.py
   ```
   This will load the documents, split them into chunks, and save these chunks to the Chroma vector store.

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
├── chroma/                     # Directory for storing Chroma vector database
├── data/                       # Directory containing data files
│   ├── books/                  # Example book files
│   │   └── alice_in_wonderland.txt
│   └── documents/              # Directory for storing documents to be processed
├── instance/                   # Directory containing main scripts
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

## JSON Format Guide

### Chat Request Format
When sending a chat message to the server, the JSON payload should follow this structure:
```json
{
  "message": "Your message here",
  "phone_number": "Your phone number here",
  // "history": [  // OPTIONAL 
  //   {
  //     "role": "user",
  //     "content": "Previous user message"
  //   },
  //   {
  //     "role": "bot",
  //     "content": "Previous bot response"
  //   }
  // ]
}
```

### Chat Response Format
The server responds with the following JSON structure:
```json
{
  "reply": "Bot's reply to the user message"
}
```

### SMS Request Format
When sending an SMS message using Africa's Talking, the JSON payload should look like this:
```json
{
  "to": "+254712345678",
  "message": "Your SMS message here"
}
```

### SMS Response Format
The response from Africa's Talking will typically be in this format:
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
