import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- 1. الصفحة الرئيسية للواجهة ---
@app.route('/')
def home():
    return render_template('index.html')

# --- 2. مسار معالجة محادثات الشات بوت ---
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json() or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please enter a message.", "reply": "Please enter a message."}), 400

        # قراءة القراءات الحية من الكاميرا
        camera_status = "System normal. No active hazard data."
        if os.path.exists("system_status.txt"):
            try:
                with open("system_status.txt", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        camera_status = content
            except Exception as e:
                print(f"[⚠️ Warning] Could not read status file: {e}")

        # حقن سياق بيانات الكاميرا في السؤال
        enhanced_prompt = f"""You are the MACMS Smart Building Assistant. Answer the user strictly using the live camera detection data provided below. Do NOT hallucinate room numbers, percentages, or unverified threats.

[LIVE CAMERA DATA]: {camera_status}

[USER QUESTION]: {user_message}"""

        # إعداد الطلب إلى Ollama (تأكدي من مطابقة اسم الموديل لما هو محمل لديك)
        payload = {
            "model": "qwen3:8b",  # استبدليه بـ llama3 أو qwen2 إذا كنتِ تستخدمين موديل آخر
            "messages": [
                {"role": "user", "content": enhanced_prompt}
            ],
            "stream": False
        }

        # إرسال الطلب لخادم Ollama
        # استبدل السطر الحالي بهذا السطر (زيادة التايم أوت إلى 120 ثانية)
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=120)

        if response.status_code == 200:
            result = response.json()
            bot_reply = result.get("message", {}).get("content", "No response generated.")
            return jsonify({"response": bot_reply, "reply": bot_reply})
        else:
            print(f"[❌ Ollama Error]: Code {response.status_code} - {response.text}")
            return jsonify({"response": "❌ I couldn't connect to the MACMS server.", "reply": "❌ I couldn't connect to the MACMS server."}), 500

    except requests.exceptions.ConnectionError:
        print("[❌ Error]: Ollama is not running at http://localhost:11434")
        return jsonify({"response": "❌ I couldn't connect to the MACMS server. Make sure Ollama is running.", "reply": "❌ I couldn't connect to the MACMS server."}), 500
    except Exception as e:
        print(f"[❌ Exception]: {e}")
        return jsonify({"response": "❌ An error occurred processing your request.", "reply": "❌ An error occurred."}), 500

# --- 3. تشغيل الخادم ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)