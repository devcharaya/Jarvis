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


def identify_speaker():
    global SESSION_OWNER

    security = load_security()
    if not security:
        return None

    owner_name = security.get("owner_name")

    if SESSION_OWNER is None:
        SESSION_OWNER = owner_name
        return owner_name

    if SESSION_OWNER == owner_name:
        return owner_name

    return None


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
