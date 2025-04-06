

def contains_stop_words(text: str, stop_words: set[str]) -> bool:
    text_words = set(text.lower().split())
    return any(word in stop_words for word in text_words)
