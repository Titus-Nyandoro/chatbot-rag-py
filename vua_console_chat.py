import requests

def send_message(message, phone='0712345678'):
    url = "http://127.0.0.1:5000/chat"  # Adjust the URL if app is hosted
    payload = {"message": message, "phone_number":phone}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        reply = response.json().get("reply")
        return reply
    else:
        print(f"Failed to get response. Status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return None

if __name__ == "__main__":
    print("Welcome to the Vua Chatbot. Type 'exit' or 'end chat' to quit.")
 
    while True:
        user_message = input("You: ")
        
        if user_message.lower() in ["exit", "end chat"]:
            print("Ending chat. Goodbye!")
            break
        
        bot_reply = send_message(user_message)
        
        if bot_reply:
            print(f"Bot: {bot_reply}")
        else:
            print("Sorry, something went wrong. Please try again.")
