import json
import time
import hashlib
import os

SECURITY_FILE = "security.json"
MAX_ATTEMPTS = 3
LOCK_DURATION = 60  # seconds


def load_security():
    if not os.path.exists(SECURITY_FILE):
        # default structure
        return {
            "pin_hash": "",
            "failed_pin_attempts": 0,
            "lock_until": 0
        }

    try:
        with open(SECURITY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {
            "pin_hash": "",
            "failed_pin_attempts": 0,
            "lock_until": 0
        }


def save_security(data):
    with open(SECURITY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()


def set_pin(pin: str):
    data = load_security()
    data["pin_hash"] = hash_pin(pin)
    save_security(data)


def is_locked():
    data = load_security()
    return time.time() < data.get("lock_until", 0)


def verify_pin(spoken_pin: str) -> bool:
    data = load_security()

    # Check lock
    if is_locked():
        return False

    if hash_pin(spoken_pin) == data.get("pin_hash"):
        data["failed_pin_attempts"] = 0
        save_security(data)
        return True

    # Wrong PIN
    data["failed_pin_attempts"] += 1

    if data["failed_pin_attempts"] >= MAX_ATTEMPTS:
        data["lock_until"] = time.time() + LOCK_DURATION
        data["failed_pin_attempts"] = 0

    save_security(data)
    return False
