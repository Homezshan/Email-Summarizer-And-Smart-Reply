from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app, origins="*")

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')

    prompt = f"Summarize this email in 3-4 sentences:\n\n{text}"

    response = model.generate_content(prompt)
    summary = response.text

    return jsonify({"summary": summary})

@app.route('/reply', methods=['POST'])
def reply():
    data = request.get_json()
    text = data.get('text', '')

    prompt = f"Write a polite, professional reply to this email:\n\n{text}"

    response = model.generate_content(prompt)
    reply_text = response.text

    return jsonify({"reply": reply_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
