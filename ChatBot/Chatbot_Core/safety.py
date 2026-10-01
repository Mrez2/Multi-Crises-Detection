def is_safe_input(text):
    """
    Validate input text type, emptiness, and length constraints.
    """
    if not text or not isinstance(text, str):
        return False
    
    cleaned_text = text.strip()
    if len(cleaned_text) == 0 or len(cleaned_text) > 1000:
        return False
        
    return True