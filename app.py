from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Create Flask app
app = Flask(__name__)

# Webhook route for POST request from Twilio
@app.route("/webhook", methods=["POST"])
def webhook():
    # Get incoming message from WhatsApp
    incoming_msg = request.values.get('Body', '').strip()
    print("User:", incoming_msg)

    # Get GPT response
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": incoming_msg}
        ]
    )
    reply = response.choices[0].message.content.strip()
    print("GPT:", reply)

    # Send reply back to WhatsApp
    twilio_response = MessagingResponse()
    msg = twilio_response.message()
    msg.body(reply)
    return str(twilio_response)

# Start server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
