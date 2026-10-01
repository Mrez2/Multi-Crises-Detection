from ollama import chat
from ChatBot.MACMS.emergency_state import emergency_state 


SYSTEM_PROMPT = """
You are the MACMS Emergency Assistant.

Your job is to help users understand the current emergency situation
and provide safety-related information.

Rules:
- Support Arabic and English.
- Respond in the same language as the user.
- Use the MACMS emergency state provided to answer questions about
  the current situation.
- Never invent or guess real-time emergency information.
- If the provided emergency state does not contain the requested
  information, clearly say that the information is unavailable.
- Be clear, concise, and accurate.
"""


def ask_macms(question):
    state_text = f"""
Current MACMS Emergency State:

{emergency_state}
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": state_text + "\nUser Question:\n" + question
            }
        ]
    )

    return response["message"]["content"]