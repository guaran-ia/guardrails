import re

def preprocess_text(text: str) -> str:
    """
    Basic preprocessing for ML models.
    """
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    return text