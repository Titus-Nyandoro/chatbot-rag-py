# Chatbot SMS python Library

Welcome to All! This guide will walk you through setting up a Python project that uses various libraries and services to create a sophisticated chatbot capable of handling SMS interactions, document parsing, and querying a database. Below you'll find detailed instructions on installing dependencies, configuring the environment, and running the application.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Install Dependencies](#install-dependencies)
- [Configuration](#configuration)
- [Creating the Database](#creating-the-database)
- [Querying the Database](#querying-the-database)
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before proceeding with the setup, ensure you have the following installed:

- **Python 3.8+**: Ensure that Python is installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
- **pip**: Python package installer should be available. Usually, it comes with Python installation.
- **conda** (optional but recommended): A package manager that simplifies managing dependencies, especially for machine learning projects. You can download it from [anaconda.com](https://www.anaconda.com/products/distribution).

## Install Dependencies

1. **Install `onnxruntime`**:
    - Due to challenges with installing `onnxruntime` via `pip`, use the following steps:

    - **For MacOS Users**:
        ```bash
        conda install onnxruntime -c conda-forge
        ```
        Refer to this [thread](https://github.com/microsoft/onnxruntime/issues/11037) for additional help if needed.

    - **For Windows Users**:
        Follow the guide [here](https://github.com/bycloudai/InstallVSBuildToolsWindows?tab=readme-ov-file) to install the Microsoft C++ Build Tools. Make sure to complete all steps to set the environment variable path correctly.

2. **Install other dependencies**:
    - Run the following command to install all dependencies listed in the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Markdown dependencies**:
    - Install dependencies for working with markdown files:
    ```bash
    pip install "unstructured[md]"
    ```

4. **Install Africastalking library**:
    - Install the Africastalking library for SMS functionality:
    ```bash
    pip install africastalking
    ```

## Configuration

1. **Set up OpenAI Key**:
    - Register for an API key at [OpenAI](https://beta.openai.com/signup/).
    - Set the OpenAI API key as an environment variable:
    ```bash
    export OPENAI_API_KEY='your_openai_api_key'
    ```

2. **Africastalking Configuration**:
    - Register at [Africastalking](https://account.africastalking.com/) to obtain your username and API key.
    - Set your Africastalking username and API key as environment variables:
    ```bash
    export AFRICASTALKING_USERNAME='your_username'
    export AFRICASTALKING_API_KEY='your_api_key'
    export AFRICASTALKING_SHORTCODE='your_sms_shortcode'
    ```

3. **System Message Configuration**:
    - Define your system message in a `system_message.txt` file located in the project root directory. This message will guide the chatbot's responses.

4. **Load PDF Documents**:
    - Ensure the `docs` folder in the project directory is populated with important PDF files. These documents will be parsed and used by the application.

## Creating the Database

Create the Chroma database by running the following script:

```bash
python create_database.py
```

## Querying the Database

Query the Chroma database with a specific question:

```bash
python query_data.py "How can vua improve my financial status?"
```

> Note: Make sure the OpenAI API key is set in your environment variables for this to work.

## Project Structure

The project is organized as follows:

```plaintext
langchain-rag-tutorial/
│
├── create_database.py  # Script to create and populate the Chroma database
├── query_data.py  # Script to query the Chroma database
├── requirements.txt  # File containing project dependencies
├── system_message.txt  # File containing the system message for the chatbot
├── docs/  # Folder containing PDF documents to be parsed
└── README.md  # Project documentation file
```

## Key Features

- **PDF Document Reader**: Parses PDF documents for information retrieval.
- **Chroma Database**: Uses Chroma DB for efficient data storage and retrieval.
- **OpenAI Integration**: Utilizes OpenAI for text embedding and completion.
- **SMS Interaction**: Handles SMS parsing and sending via Africastalking.


## Usage

1. **Sending SMS**:
    - Call the `send_sms` function with an `SmsRequest` object to send an SMS.

2. **Receiving SMS**:
    - Configure your SMS gateway to forward messages to your application's receiving endpoint.
    - The application will process incoming messages automatically using the `process_incoming_sms` function.

3. **Loading PDF Documents**:
    - Populate the `docs` folder with PDF files containing important information. The application will parse these files as needed.

4. **Querying the Database**:
    - Use `query_data.py` to query the Chroma database with specific questions.

5. **SMS Processing**:
    - Incoming SMS messages are processed to generate responses. Phone numbers are reformatted to the standard `+254` format, and a response is sent back to the user.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes. Ensure your code adheres to the project’s coding standards and includes relevant tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README provides a comprehensive guide for setting up, using, and contributing to the Langchain RAG Tutorial. Feel free to reach out if you have any questions or need further assistance. Happy coding! 🚀

