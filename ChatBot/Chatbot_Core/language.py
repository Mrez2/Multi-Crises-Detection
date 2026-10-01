import re

def detect_language(text):
    """
    Detect whether the input message is in Arabic or English.
    """
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    if arabic_pattern.search(text):
        return "ar"
    return "en"