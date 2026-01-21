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
    "briefly", "in", "detail", "please", "can", "you"
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
    key = normalize_prompt(prompt)

    if key in AI_CACHE:
        return AI_CACHE[key]
    
    global LAST_AI_CALL_TIME

    now = time.time()
    if now - LAST_AI_CALL_TIME < AI_COOLDOWN_SECONDS:
        return "Please wait a moment, I'm thinking."

    LAST_AI_CALL_TIME = now
    try:
        with requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": prompt,
                "stream": True,
                "options": {
                    "num_predict": 60 if idle else 60
                }
            },
            stream=True,
            timeout=AI_TIMEOUT
        ) as r:

            if r.status_code != 200:
                return AI_FALLBACK_MESSAGE

            collected = ""
            start = time.time()

            for line in r.iter_lines():
                # stop if timeout reached
                if time.time() - start > AI_TIMEOUT:
                    break

                if not line:
                    continue

                try:
                    data = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError:
                    continue

                if "response" in data:
                    collected += data["response"]

                if len(collected) >= MAX_RESPONSE_CHARS:
                    break

            final_answer = collected.strip()

            if final_answer:
                AI_CACHE[key] = final_answer

                if len(AI_CACHE) > MAX_CACHE_SIZE:
                    AI_CACHE.pop(next(iter(AI_CACHE)))

            return final_answer if final_answer else AI_FALLBACK_MESSAGE


    except Exception:
        return AI_FALLBACK_MESSAGE
