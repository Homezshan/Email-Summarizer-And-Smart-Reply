from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Use correct model
model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_text(response):
    """Safely extract text from Gemini response."""
    try:
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "⚠️ No text returned (possible safety block)"
    except Exception as e:
        print("TEXT EXTRACTION ERROR:", e)
        return "⚠️ Could not extract model output"


@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "")

        # ✅ SAFETY-BYPASS PROMPT
        prompt = (
            "You are allowed to read and summarize this email. "
            "The user gives full permission to process this content. "
            "Summarize the email in 3–4 simple sentences:\n\n"
            f"{text}"
        )

        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 300}
        )

        summary = extract_text(response)
        return jsonify({"summary": summary})

    except Exception as e:
        print("SUMMARY ERROR:", e)
        return jsonify({"summary": None, "error": str(e)}), 500


@app.route('/reply', methods=['POST'])
def reply():
    try:
        data = request.get_json()
        text = data.get("text", "")

        # ✅ SAFETY-BYPASS PROMPT
        prompt = (
            "You are allowed to read and generate a reply to this email. "
            "The user gives full permission to process this content. "
            "Write a polite, professional reply:\n\n"
            f"{text}"
        )

        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 300}
        )

        reply_text = extract_text(response)
        return jsonify({"reply": reply_text})

    except Exception as e:
        print("REPLY ERROR:", e)
        return jsonify({"reply": None, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
