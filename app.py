import os
import requests
import webbrowser
import threading
from flask import Flask, request, jsonify, send_from_directory
from ChatBot.Chatbot_Core.response_generator import build_ai_prompt

app = Flask(__name__)


# =========================
# الصفحة الرئيسية
# =========================

@app.route("/")
def home():
    try:
        return send_from_directory("templates", "index.html")
    except Exception:
        return send_from_directory(".", "index.html")


# =========================
# محادثة الشات بوت
# =========================

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    # بناء السياق
    base_prompt = build_ai_prompt(user_message)

    # توجيه صارم يمنع طباعة أي مبررات أو لغات غريبة
    system_instructions = (
        "You are the MACMS Assistant. "
        "Rule 1: Respond directly in the EXACT SAME language as the user input (Arabic for Arabic, English for English). "
        "Rule 2: Do NOT output internal thoughts, reasoning notes, or any Chinese text. "
        "Rule 3: Output ONLY the final response to the user.\n\n"
    )

    full_prompt = system_instructions + base_prompt

    payload = {
        "model": "qwen2.5:7b",
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "num_predict": 100,
            "num_ctx": 1024,
            "temperature": 0.1,  # درجة حرارة منخفضة تمنع الهلوسة وتسريب تفكير الموديل
            "top_k": 20
        }
    }

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        bot_response = result.get("response", "").strip()

        return jsonify({"response": bot_response})

    except requests.exceptions.ConnectionError:
        return jsonify({"response": "❌ Could not connect to Ollama. Make sure Ollama is running."}), 500
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"response": "❌ Error generated while processing."}), 500


# =========================
# فتح متصفح Chrome تلقائياً
# =========================

def open_chrome():
    url = "http://127.0.0.1:5000/"
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    try:
        webbrowser.get(chrome_path).open(url)
    except Exception:
        webbrowser.open(url)


# =========================
# تشغيل السيرفر
# =========================

if __name__ == "__main__":
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(1.2, open_chrome).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )