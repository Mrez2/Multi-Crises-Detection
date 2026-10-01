import threading
import time
import cv2
import telebot
from ultralytics import YOLO

# استيراد خدمات التنبيهات
from ChatBot.bot_instance import bot, CHAT_ID
from ChatBot.Services.alert_service import send_image_alert
from ChatBot.Speech.voice_service import send_voice_alert
from danger_analyzer import DangerAnalyzer
from utils.logger import log_event

# استيراد تطبيق الشات بوت
from app import app 

# --- تشغيل بوت تليجرام ---
def start_bot_thread():
    try:
        bot.get_me()
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"\n[⚠️] Telegram Bot Error: {e}")

threading.Thread(target=start_bot_thread, daemon=True).start()

# --- تشغيل خادم الشات بوت ---
def start_flask_server():
    try:
        print("\n🚀 Starting MACMS Web Assistant on port 5000...")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"\n[⚠️] Flask Server Error: {e}")

threading.Thread(target=start_flask_server, daemon=True).start()

# --- ربط نماذج الذكاء الاصطناعي ---
fire_model = YOLO("best.pt")   # نموذجك المخصص لاكتشاف الحريق
person_model = YOLO("yolov8n.pt") 

danger = DangerAnalyzer()
last_alert_time = 0
ALERT_COOLDOWN = 10 

def process_frame(frame):
    global last_alert_time
    fire_results = fire_model(frame, conf=0.35, verbose=False)
    person_results = person_model(frame, classes=[0], conf=0.40, verbose=False)

    annotated = fire_results[0].plot(img=frame.copy())
    fire_count, smoke_count, people_count = 0, 0, 0

    # 1. كشف الحريق والدخان
    for box in fire_results[0].boxes:
        cls = int(box.cls[0])
        if cls == 0: smoke_count += 1
        elif cls == 1: fire_count += 1

    # 2. كشف ورسم الأشخاص (المسافات البادئة صحيحة هنا)
    for box in person_results[0].boxes:
        people_count += 1
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 3. تحليل الخطورة وحفظ البيانات للحاسوب والشات بوت
    level, color = danger.analyze(fire_count, smoke_count, people_count)
    
    try:
        with open("system_status.txt", "w", encoding="utf-8") as f:
            f.write(f"Status: {level} | Fire Detected: {fire_count} | Smoke Detected: {smoke_count} | People Detected: {people_count}")
    except Exception:
        pass

    annotated = danger.draw_panel(annotated, fire_count, smoke_count, people_count, level, color)

    # 4. إرسال التنبيهات عند الخطر
    current_time = time.time()
    if level in ["HIGH RISK", "CRITICAL", "HIGH"] and (current_time - last_alert_time > ALERT_COOLDOWN):
        last_alert_time = current_time
        cv2.imwrite("temp_alert.jpg", annotated)
        max_conf = float(fire_results[0].boxes.conf.max()) if len(fire_results[0].boxes) > 0 else 0.35
        caption = f"⚠️ **تحذير خطورة عالية!**\n🔥 حريق: {fire_count}\n💨 دخان: {smoke_count}\n👥 أشخاص: {people_count}"
        
        try:
            send_image_alert("temp_alert.jpg", max_conf, caption)
            send_voice_alert(CHAT_ID, text="تحذير! تم الكشف عن خطر حريق داخل المبنى")
        except Exception as e:
            print(f"Alert Error: {e}")

    return annotated

def camera_mode():
    cap = cv2.VideoCapture(0)
    frame_count = 0
    last_annotated_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            break

        frame_count += 1
        
        # معالجة إطار واحد كل 3 إطارات لتخفيف الضغط على المعالج
        if frame_count % 3 == 0 or last_annotated_frame is None:
            last_annotated_frame = process_frame(frame)

        cv2.imshow("Smart Building Monitor", last_annotated_frame)
        
        if cv2.waitKey(1) == ord("q"): 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("\n SMART BUILDING SYSTEM STARTED")
    camera_mode()