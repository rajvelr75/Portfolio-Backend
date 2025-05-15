from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
CORS(app, origins=["https://portfolio-2-ao4.pages.dev"])

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

portfolio_info = """
You are a chatbot for Rajvel's personal portfolio. Only answer questions related to:
- Rajvel's projects, skills, education, experience, resume, and contact info.
If the question is not about the portfolio, reply: "I'm only here to help with portfolio-related queries."
"""

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    try:
        convo = model.start_chat()
        convo.send_message(f"{portfolio_info}\n\nUser: {user_input}")
        response = convo.last.text
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"reply": "Something went wrong."}), 500

if __name__ == '__main__':
    app.run()
