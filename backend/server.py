from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini API key
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "")

        prompt = f"Summarize this email:\n\n{text}"

        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 400}
        )

        return jsonify({"summary": response.text})

    except Exception as e:
        print("SUMMARY ERROR:", str(e))
        return jsonify({"summary": None, "error": str(e)}), 500


@app.route("/reply", methods=["POST"])
def reply():
    try:
        data = request.get_json()
        text = data.get("text", "")

        prompt = f"Write a polite reply to this email:\n\n{text}"

        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 400}
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        print("REPLY ERROR:", str(e))
        return jsonify({"reply": None, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
