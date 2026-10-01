import datetime

def log_event(event_message):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("system_log.txt", "a", encoding="utf-8") as file:
        file.write(f"[{time_now}] {event_message}\n")