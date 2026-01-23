from langdetect import detect

def detect_language(text):
    try:
        lang = detect(text)
        return "hi" if lang == "hi" else "en"
    except:
        return "en"
