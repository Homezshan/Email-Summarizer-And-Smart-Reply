from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app, origins="*")

summarizer = pipeline("summarization", model="google/flan-t5-small")



@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data['text']
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    return jsonify({'summary': summary})

@app.route('/reply', methods=['POST'])
def reply():
    data = request.get_json()
    text = data['text']
    reply_text = f"Thank you for your email regarding: \"{text[:60]}...\". I’ll get back to you shortly."
    return jsonify({'reply': reply_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
