import cv2
import datetime
import os
from ChatBot.bot_instance import CHAT_ID, bot

# Variable to track the timestamp of the last dispatched alert (cooldown mechanism)
last_alert_time = 0

def send_image_alert(frame, confidence, alert_type="Fire"):
    """
    Capture the current camera frame and dispatch an alert report via Telegram.
    
    :param frame: Camera image frame (NumPy Array)
    :param confidence: Model confidence score percentage (e.g., 85.5)
    :param alert_type: Detected threat category (e.g., Fire / Intruder)
    """
    global last_alert_time
    
    current_timestamp = datetime.datetime.now().timestamp()
    
    # Cooldown check: Ensure at least 10 seconds pass between consecutive alerts
    if current_timestamp - last_alert_time < 10:
        return

    # Update last alert timestamp
    last_alert_time = current_timestamp

    # 1. Format current timestamp
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    
    # 2. Construct alert caption report
    caption_text = (
        f"🚨 **NEW EMERGENCY ALERT!** 🚨\n\n"
        f"⚠️ **Type:** Detected {alert_type}\n"
        f"🎯 **Confidence:** {confidence:.1f}%\n"
        f"🕒 **Timestamp:** {time_now}\n"
        f"📍 **Location:** Main Surveillance Camera\n\n"
        f"ℹ️ *Please take immediate action and verify facility safety.*"
    )

    # 3. Save the current frame temporarily
    temp_image_path = "temp_alert.jpg"
    cv2.imwrite(temp_image_path, frame)

    try:
        # 4. Dispatch image and formatted report via Telegram
        with open(temp_image_path, "rb") as photo:
            bot.send_photo(
                chat_id=CHAT_ID,
                photo=photo,
                caption=caption_text,
                parse_mode="Markdown"
            )
        print("✅ Image alert sent successfully!")
        
    except Exception as e:
        print(f"❌ Error sending image alert: {e}")
        
    finally:
        # 5. Clean up temporary image file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        


