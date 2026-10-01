import os
from gtts import gTTS
from ChatBot.bot_instance import bot

def send_voice_alert(chat_id, text):
    """Convert hazard alert text to voice audio and dispatch via Telegram."""
    try:
        tts = gTTS(text=text, lang='en')
        audio_path = "temp_audio.wav"
        tts.save(audio_path)
        
        with open(audio_path, 'rb') as audio:
            bot.send_voice(chat_id, audio)
            
        if os.path.exists(audio_path):
            os.remove(audio_path)
    except Exception as e:
        print(f"[⚠️ Voice Alert Error]: {e}")