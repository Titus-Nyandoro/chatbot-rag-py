from flask import Flask, request, jsonify, session, Response
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import africastalking
import os
import openai
from dotenv import load_dotenv

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()

app = Flask(__name__)
app.secret_key = "vua_app_secret_key"

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Africa's Talking
africastalking.initialize(username='sandbox', api_key='')
sms = africastalking.SMS

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
You are VUA assistant, a polite AI assistant.
You're assisting with questions about a VUA SOLUTIONS LIMITED Financial product.
Use the information from the DOCUMENTS section to provide accurate answers.
The answers should be a short 144 character long response.
The output language should be in English.
If unsure ,simply state that you don't know.
for all request regarding, contacts, location, & address,
refer to this:
            P.O. BOX 10199, G.P.O NAIROBI,
            TELEPHONE: +254724396442,
            EMAIL: vualimited@gmail.com,
            LOCATION: MOMBASA, KENYA,
            STREET: Polepole Road, E-Learning Building

Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Prepare the DB.
embedding_function = OpenAIEmbeddings()
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

@app.route('/')
def hello_world():
    return 'Hello from Vua!'

def get_bot_response(user_message):
    conversation_history = session.get('conversation_history', [])
    conversation_history.append({"role": "user", "content": user_message})

    results = db.similarity_search_with_relevance_scores(user_message, k=3)
    # if not results or results[0][1] < 0.7:
    #     bot_reply = "I'm sorry, I couldn't find any relevant information."
    # else:
    #     context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, score in results if score > 0.7])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_message)

    # model = ChatOpenAI()
    model = ChatOpenAI(model="gpt-4-1106-preview")


    response = model.invoke(prompt)
    bot_reply = response.content

    conversation_history.append({"role": "assistant", "content": bot_reply})
    session['conversation_history'] = conversation_history

    return bot_reply

@app.route('/send-sms', methods=['GET'])
def send_sms():
    recipient = request.args.get('to')
    if not recipient:
        return 'Please provide a recipient number.'

    if recipient.startswith('0'):
        recipient = '+254' + recipient[1:]
    elif recipient.startswith('+'):
        if not recipient.startswith('+254'):
            return 'Recipient number must have the country code for Kenya (+254).'
    else:
        return 'Recipient number must include the country code for Kenya (+254).'

    if len(recipient) != 13:
        return 'Please provide a valid phone number. (0712345678 | 0123456789)'

    message = "Hey welcome to Vua!"
    sender = "88555"
    try:
        response = sms.send(message, [recipient], sender)
        return response
    except Exception as e:
        return f'Houston, we have a problem: {e}'

@app.route('/chat', methods=["POST"])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    bot_reply = get_bot_response(user_message)

    return jsonify({"reply": bot_reply})

@app.route('/vua', methods=['POST'])
def incoming_messages():
    message_data = request.form  # Get data from Africa's Talking POST request
    message = message_data.get('text', '').lower()
    phone_number = message_data.get('from', '')

    if not message or not phone_number:
        return Response(status=400)

    print(f"Received message: {message} from {phone_number}")

    bot_reply = get_bot_response(message)

    # Send the reply via SMS
    try:
        response = sms.send(bot_reply, [phone_number], "88555")
        print(f"Sent reply: {bot_reply} to {phone_number}")
        return Response(status=200)
    except Exception as e:
        print(f"Failed to send SMS reply: {e}")
        return Response(status=500)

@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.get_json(force=True)
    print(f'Delivery report response...\n {data}')
    return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True)
