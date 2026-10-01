import os
from ChatBot.bot_instance import bot
from ChatBot.chatbot import ask_macms
from ChatBot.Speech.speech_service import transcribe_audio

# 1. استقبال النصوص من تليجرام
@bot.message_handler(content_types=['text'])
def handle_text(message):
    response = ask_macms(message.text)
    bot.reply_to(message, response)

# 2. استقبال الصوت من تليجرام
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        bot.reply_to(message, "🎙️ Processing voice note...")
        
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        ogg_path = "user_voice.ogg"
        with open(ogg_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        # تحويل الصوت لنص ثم إرساله لـ Ollama
        transcribed_text = transcribe_audio(ogg_path)
        if os.path.exists(ogg_path):
            os.remove(ogg_path)

        bot.send_message(message.chat.id, f"🗣️ Transcribed: \"{transcribed_text}\"")
        
        # الحصول على الرد من المحرك الموحد
        response = ask_macms(transcribed_text)
        bot.send_message(message.chat.id, response)

    except Exception as e:
        bot.reply_to(message, f"❌ Voice processing error: {e}")