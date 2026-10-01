import os

def get_emergency_state():
    """Retrieve live camera data from shared system status file."""
    if os.path.exists("system_status.txt"):
        try:
            with open("system_status.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return content
        except Exception as e:
            print(f"[⚠️ Emergency State Error]: {e}")
            
    return "Status: SAFE | Fire Detected: 0 | Smoke Detected: 0 | People Detected: 0"

def get_status_text():
    """Supply formatted live status for AI prompt construction."""
    return get_emergency_state()