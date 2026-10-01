from ChatBot.chatbot import ask_macms


questions = [
    "هل يوجد حريق حاليًا؟",
    "فين الحريق؟",
    "كام شخص لسه جوه؟",
    "What is the severity?",
    "What is the temperature?"
]


for question in questions:
    print("\n" + "=" * 60)
    print("USER:", question)
    print("-" * 60)

    answer = ask_macms(question)

    print("ASSISTANT:", answer)