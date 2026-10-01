from safety import is_safe_input
from language import detect_language
from response_generator import build_ai_prompt

def route_message(user_message):
    """
    Route user message, validate safety, and generate the final structured prompt.
    """
    if not is_safe_input(user_message):
        return None, "Invalid or unsafe message content."

    lang = detect_language(user_message)
    prompt = build_ai_prompt(user_message, lang)
    
    return prompt, None