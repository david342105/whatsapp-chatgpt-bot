from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    print("User:", incoming_msg)

# Get GPT response
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": incoming_msg}
    ]
)

reply = response.choices[0].message.content.strip()


    print("GPT:", reply)

    # Send reply to WhatsApp
    twilio_response = MessagingResponse()
    msg = twilio_response.message()
    msg.body(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

