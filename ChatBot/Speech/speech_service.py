import os
import whisper
import static_ffmpeg

# تفعيل محرك الصوت تلقائياً
static_ffmpeg.add_paths()

# تحميل نموذج Whisper المحلي
try:
    print("⏳ Loading Whisper offline model...")
    model = whisper.load_model("base")
    print("✅ Whisper model loaded successfully.")
except Exception as e:
    model = None
    print(f"❌ Whisper Load Error: {e}")

def transcribe_audio(audio_path, language="ar-EG"):
    """
    Transcribe speech from audio file (.wav) using offline OpenAI Whisper.
    """
    if not os.path.exists(audio_path) or model is None:
        return ""

    try:
        lang_code = "ar" if "ar" in language.lower() else "en"
        result = model.transcribe(audio_path, language=lang_code)
        text = result.get("text", "").strip()
        print(f"🎙️ [Offline Speech-to-Text Success]: \"{text}\"")
        return text
    except Exception as e:
        print(f"❌ [Offline STT Error]: {e}")
        return ""