from flask import Flask, request, jsonify, session, Response
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.summarize import load_summarize_chain
import africastalking
import os
import openai
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON
import logging
from datetime import datetime
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")  # sqlite:///vua.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize databases
db = SQLAlchemy(app)

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Africa's Talking
africastalking.initialize(username=os.getenv("AT_USERNAME"), api_key=os.getenv("AT_API_KEY"))
sms = africastalking.SMS

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
You are Vua AI Assistant, the friendly and knowledgeable chatbot for Vua. At Vua, we are dedicated to empowering underserved communities with seamless financial services. Our mission is to help individuals take control of their finances and create financially sustainable lifestyles. We offer savings accounts, loans, and investment opportunities to help our customers achieve financial freedom.

Answer the question based on the following context and the user's profile:

Context: {context}
User Profile: {profile}

Previous Conversation Summary: {summary}

Question: {question}
"""

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    profile = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.Column(JSON)
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

# Prepare the Vector DB
embedding_function = OpenAIEmbeddings()
db_chroma = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

# Helper Functions
def get_or_create_user(phone_number):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        user = User(phone_number=phone_number, profile={})
        db.session.add(user)
        db.session.commit()
    return user

def update_user_profile(user, new_data):
    user.profile.update(new_data)
    db.session.commit()

def get_conversation_summary(conversation):
    if not conversation.summary:
        chain = load_summarize_chain(ChatOpenAI(temperature=0), chain_type="map_reduce")
        conversation.summary = chain.run(conversation.messages)
        db.session.commit()
    return conversation.summary

def get_bot_response(user_message, user):
    # Get or create conversation
    conversation = Conversation.query.filter_by(user_id=user.id).order_by(Conversation.created_at.desc()).first()
    if not conversation:
        conversation = Conversation(user_id=user.id, messages=[])
        db.session.add(conversation)
    
    # Append user message
    conversation.messages.append({"role": "user", "content": user_message})
 
    # print("conversation")
    # print(conversation.messages)
 
    
    # Search in Chroma
    results = db_chroma.similarity_search_with_relevance_scores(user_message + " " + json.dumps(user.profile), k=3)

    # print(results)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, score in results if score > 0.7])
    
    # Get conversation summary
    summary = get_conversation_summary(conversation)
    
    # Generate response
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, profile=json.dumps(user.profile), summary=summary, question=user_message)
    
    model = ChatOpenAI(model="gpt-3.5-turbo-1106")
    response = model.invoke(prompt)
    bot_reply = response.content
    
    # Append bot reply and save
    conversation.messages.append({"role": "assistant", "content": bot_reply})
    db.session.commit()
    
    return bot_reply

def send_sms(message, recipient):
    try:
        response = sms.send(message, [recipient], "88555")
        logger.info(f"SMS sent to {recipient}: {response}")
    except Exception as e:
        logger.error(f"Failed to send SMS to {recipient}: {e}")

# Routes
@app.route('/')
def hello_world():
    return 'Hello from Vua!'

@app.route('/send-sms', methods=['GET'])
def send_sms_route():
    recipient = request.args.get('to')
    if not recipient:
        return 'Please provide a recipient number.'

    if recipient.startswith('0'):
        recipient = '+254' + recipient[1:]
    elif not recipient.startswith('+254'):
        return 'Recipient number must have the country code for Kenya (+254).'

    if len(recipient) != 13:
        return 'Please provide a valid phone number. (0712345678 | 0123456789)'

    message = "Hey welcome to Vua!"
    send_sms(message, recipient)
    return 'SMS sent.'

@app.route('/chat', methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    phone_number = data.get('phone_number')
    
    if not user_message or not phone_number:
        return jsonify({"error": "Message and phone number required"}), 400

    user = get_or_create_user(phone_number)
    bot_reply = get_bot_response(user_message, user)

    return jsonify({"reply": bot_reply})

@app.route('/vua', methods=['POST'])
def incoming_messages():
    message_data = request.form
    message = message_data.get('text', '').lower()
    phone_number = message_data.get('from', '')

    if not message or not phone_number:
        return Response(status=400)

    logger.info(f"Received message: {message} from {phone_number}")

    user = get_or_create_user(phone_number)
    bot_reply = get_bot_response(message, user)

    send_sms(bot_reply, phone_number)
    return Response(status=200)

@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.get_json(force=True)
    logger.info(f'Delivery report response: {data}')
    return Response(status=200)

@app.route('/update-profile', methods=['POST'])
def update_profile_route():
    data = request.get_json()
    phone_number = data.get('phone_number')
    profile_data = data.get('profile')
    
    if not phone_number or not profile_data:
        return jsonify({"error": "Phone number and profile data required"}), 400

    user = get_or_create_user(phone_number)
    update_user_profile(user, profile_data)
    return jsonify({"message": "Profile updated successfully"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)