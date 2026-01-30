import requests
import time
import json

AI_TIMEOUT = 15          # seconds
MAX_RESPONSE_CHARS = 300
AI_CACHE = {}
MAX_CACHE_SIZE = 20
AI_COOLDOWN_SECONDS = 5
LAST_AI_CALL_TIME = 0


AI_FALLBACK_MESSAGE = "I'm having trouble thinking right now. Please try again in a moment."



OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

COMMON_FILLER_WORDS = {
    "what", "is", "explain", "tell", "me", "about",
    "briefly", "in", "detail", "please", "can", "you","why"
}



def normalize_prompt(text: str) -> str:
    words = text.lower().strip().split()

    filtered = [
        w for w in words
        if w not in COMMON_FILLER_WORDS
    ]

    return " ".join(filtered)

def warmup_ai():
    try:
        requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": "hello",
                "stream": False,
                "options": {"num_predict": 1}
            },
            timeout=5
        )
    except:
        pass


def ask_ai(prompt: str, idle: bool = False) -> str:

    if len(prompt.strip().split()) < 2:
        return "Please ask a complete question."

    key = prompt.lower().strip()

    if key in AI_CACHE:
        return AI_CACHE[key]

    global LAST_AI_CALL_TIME
    now = time.time()

    if now - LAST_AI_CALL_TIME < AI_COOLDOWN_SECONDS:
     time.sleep(1)

    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": prompt,
                "stream": False,
                "options": {
                            "num_predict": 180,
                            "temperature": 0.3,
                            "top_p": 0.9
                           }
            },
            timeout=AI_TIMEOUT
        )

        r.raise_for_status()

        data = r.json()
        final_answer = data.get("response", "").strip()

        if not final_answer or len(final_answer) < 5:
            return "I'm thinking... try asking again."


        if final_answer:
            LAST_AI_CALL_TIME = time.time()
            AI_CACHE[key] = final_answer

            if len(AI_CACHE) > MAX_CACHE_SIZE:
                AI_CACHE.pop(list(AI_CACHE.keys())[0])

            return final_answer

        return AI_FALLBACK_MESSAGE

    except Exception:
        return AI_FALLBACK_MESSAGE
