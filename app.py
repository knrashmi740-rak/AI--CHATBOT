import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# =========================
# Upload settings
# =========================
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# Groq API
# =========================
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)
# =========================
# Home Page
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# Chat Route
# =========================
@app.route("/get")
def chatbot():

    user_msg = request.args.get("msg")

    if not user_msg:
        return jsonify({
            "reply": "Please enter a message."
        })

    try:

        response = client.chat.completions.create(

            model="meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[
                {
                    "role": "system",
                    "content": """
You are R-AI, a multilingual AI assistant.

Rules:
- Detect the language automatically.
- Reply in the same language the user uses.
- Support English, Kannada, Hindi, Tamil, Telugu and other languages.
- If the user mixes languages, reply in the same mixed style.
- Be polite, friendly and helpful.
- Keep technical explanations simple and clear.
"""
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("Groq Error:", e)

        return jsonify({
            "reply": "Sorry, I couldn't process your request. Please try again."
        })

# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)