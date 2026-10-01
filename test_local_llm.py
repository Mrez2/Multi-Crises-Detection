from ollama import chat


SYSTEM_PROMPT = """
You are the MACMS Emergency Assistant.

MACMS is a Multi-Agent Crisis Management System designed to help monitor
and manage emergency situations.

Your responsibilities:
- Answer questions related to emergency monitoring, fire incidents,
  evacuation, safety procedures, and system status.
- Support both Arabic and English.
- Always respond in the same language used by the user.
- Be concise, clear, and helpful.
- Never invent or guess real-time emergency information.
- If real-time information is not provided by the MACMS system, clearly
  say that you do not have access to the current emergency state.
- Do not claim that a fire, smoke, evacuation, or emergency is happening
  unless the MACMS system provides that information.
"""


def ask_llm(question):
    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]


questions = [
    "ما هو دورك في نظام MACMS؟",
    "What should people do during a fire emergency?",
    "هل يوجد حريق حاليًا في المبنى؟"
]

for question in questions:
    print("\n" + "=" * 60)
    print("USER:", question)
    print("-" * 60)
    print("ASSISTANT:", ask_llm(question))