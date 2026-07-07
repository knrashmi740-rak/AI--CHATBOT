import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from tavily import TavilyClient

# =========================
# Flask App
# =========================

app = Flask(__name__)

conversation_history = []

# =========================
# Upload Folder
# =========================

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# Groq Client
# =========================

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)
tavily = TavilyClient(
    api_key=os.environ.get("TAVILY_API_KEY")
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
    web_context = ""

    try:
        search = tavily.search(
           query=user_msg,
           max_results=3
        )

        for item in search["results"]:
           web_context += f"""
    Title: {item['title']}
    Content: {item['content']}
    Source: {item['url']}

    """
    except:
         pass

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
- Detect the user's language automatically.
- Reply in the same language.
- Support English, Kannada, Hindi, Tamil, Telugu and other languages.
- If the user mixes languages, reply in the same mixed style.
- Be friendly, helpful and professional.
- Explain technical concepts clearly.
"""
                },
                {
    "role": "user",
    "content": f"""
User Question:
{user_msg}

Latest Web Search Results:
{web_context}

Instructions:
- If the web search contains relevant information, use it to answer.
- If the web search is not relevant or empty, answer using your own knowledge.
"""
}
            ]

        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("Groq Error:", repr(e))

        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        })

# =========================
# Run App
# =========================

if __name__ == "__main__":
    app.run(debug=True)