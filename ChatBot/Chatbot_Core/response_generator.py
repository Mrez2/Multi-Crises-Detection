import os
from ChatBot.RAG.retriever import retriever

def get_status_text():
    """Read live camera detection data from shared status file."""
    if os.path.exists("system_status.txt"):
        try:
            with open("system_status.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return content
        except Exception:
            pass
    return "Status: SAFE | Fire Detected: 0 | Smoke Detected: 0 | People Detected: 0"

def build_ai_prompt(user_question, lang="en"):
    """Combine live camera status, modular RAG context, and user query."""
    building_state = get_status_text()
    
    # استرجاع النصوص باستخدام RAGRetriever الموديلار
    safety_guidelines = retriever.retrieve(user_question)

    prompt = f"""You are MACMS, a smart building emergency assistant. Answer the user strictly using the live camera detection data and safety protocols provided below. Do NOT hallucinate room numbers, percentages, or unverified threats.

[LIVE CAMERA DATA]: {building_state}
[SAFETY PROTOCOLS & RAG CONTEXT]: {safety_guidelines if safety_guidelines else "No specific context retrieved."}

[USER QUESTION]: {user_question}"""

    return prompt