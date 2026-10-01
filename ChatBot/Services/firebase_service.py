import os
import firebase_admin
from firebase_admin import credentials, messaging

# 1. Specify the path to the Firebase Service Account Key file
KEY_PATH = r"D:\Multi-Crises-Detection-main\Multi-Crises-Detection\fir-service-14379-firebase-adminsdk-fbsvc-5642e04d85.json"

# 2. Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    if os.path.exists(KEY_PATH):
        cred = credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)
        print("✅ Connected to Firebase server successfully!")
    else:
        print(f"⚠️ Warning: Key file '{KEY_PATH}' not found. Firebase notifications disabled.")


def send_firebase_alert(title, body, topic="emergency_alerts", image_url=None):
    """
    Dispatch real-time push notifications to mobile devices via Firebase FCM.
    
    :param title: Notification title (e.g., "🚨 Emergency Alert: Fire Detected!")
    :param body: Notification text (e.g., "Fire detected on Main Camera with 85% confidence")
    :param topic: Target topic name subscribed by mobile apps
    :param image_url: Optional image URL attachment
    """
    if not firebase_admin._apps:
        print("❌ Notification not sent: Firebase server not connected.")
        return

    try:
        # Construct basic notification payload
        notification = messaging.Notification(
            title=title,
            body=body,
            image=image_url
        )

        # Construct message targeted at topic subscribers
        message = messaging.Message(
            notification=notification,
            data={
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "alert_type": "FIRE",
                "priority": "HIGH"
            },
            topic=topic,
        )

        # Dispatch message via FCM
        response = messaging.send(message)
        print(f"🚀 Firebase notification sent successfully (Message ID: {response})")

    except Exception as e:
        print(f"❌ Error sending Firebase notification: {e}")