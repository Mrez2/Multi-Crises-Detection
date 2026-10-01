import os
import speech_recognition as sr

def transcribe_audio(audio_path, language="en-US"):
    """
    Transcribe speech from an audio file (.wav) into text using SpeechRecognition.
    
    :param audio_path: Path to the input audio file (.wav format).
    :param language: Language code for recognition (default: 'en-US', supports 'ar-EG').
    :return: Recognized text string or None if transcription fails.
    """
    recognizer = sr.Recognizer()

    if not os.path.exists(audio_path):
        print(f"[⚠️ SpeechRecognition Error]: File not found at '{audio_path}'")
        return None

    try:
        with sr.AudioFile(audio_path) as source:
            # Adjust for ambient background noise before recording
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

        # Recognize speech using Google Speech Recognition Engine
        text = recognizer.recognize_google(audio_data, language=language)
        print(f"🎙️ [Speech-to-Text Success]: \"{text}\"")
        return text

    except sr.UnknownValueError:
        print("⚠️ [SpeechRecognition Warning]: Speech was unintelligible or silent.")
        return None
    except sr.RequestError as e:
        print(f"❌ [SpeechRecognition Error]: Service request failed; {e}")
        return None
    except Exception as e:
        print(f"❌ [SpeechRecognition Error]: Unexpected processing error: {e}")
        return None