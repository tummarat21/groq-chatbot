import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ใช้ Environment Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_secret_token")

@app.route("/", methods=["GET"])
def home():
    return "Groq Chatbot is running!", 200

@app.route("/api/webhook", methods=["GET"])
def verify():
    """ Verify webhook for Facebook Messenger """
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token_sent == VERIFY_TOKEN:
        return challenge, 200
    return "Invalid verification token", 403

@app.route("/api/chat", methods=["POST"])
def chat():
    """ รับข้อความจากผู้ใช้และตอบกลับ """
    data = request.json
    user_message = data.get("message", "")

    # ใช้ Groq API
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": user_message}]
    }

    response = requests.post("https://api.groq.com/v1/chat/completions", json=payload, headers=headers)
    reply = response.json()["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})

# Export handler สำหรับ Vercel
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

