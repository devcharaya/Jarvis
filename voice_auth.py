import json
import os

SECURITY_FILE = "security.json"

SESSION_OWNER = None

SESSION_GREETED = False

def load_security():
    if not os.path.exists(SECURITY_FILE):
        return None
    with open(SECURITY_FILE, "r") as f:
        return json.load(f)



def reset_session():
    global SESSION_OWNER
    SESSION_OWNER = None
    SESSION_GREETED= False

def register_owner(name: str):
    if not os.path.exists(SECURITY_FILE):
        data = {}
    else:
        with open(SECURITY_FILE, "r") as f:
            data = json.load(f)

    data["owner_name"] = name
    with open(SECURITY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def delete_owner():
    if not os.path.exists(SECURITY_FILE):
        return

    with open(SECURITY_FILE, "r") as f:
        data = json.load(f)

    data.pop("owner_name", None)

    with open(SECURITY_FILE, "w") as f:
        json.dump(data, f, indent=2)

SECRET_PHRASE = "I am the owner"

def verify_voice_phrase(spoken_text: str) -> bool:
    return SECRET_PHRASE.lower() in spoken_text.lower()