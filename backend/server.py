from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("models/gemini-2.5-flash")

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "")

        prompt = f"Summarize this email clearly:\n\n{text}"

        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 300}
        )

        return jsonify({"summary": response.text})

    except Exception as e:
        print("SUMMARY ERROR:", e)
        return jsonify({"summary": None, "error": str(e)}), 500


@app.route("/reply", methods=["POST"])
def reply():
    try:
        data = request.get_json()
        text = data.get("text", "")

        prompt = f"Write a polite professional reply:\n\n{text}"

        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 300}
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        print("REPLY ERROR:", e)
        return jsonify({"reply": None, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
