import base64
import hashlib

SECRET_KEY = "jarvis_dev_private_key"

def _derive_key():
    """
    Derive a fixed-length key from the secret.
    """
    return hashlib.sha256(SECRET_KEY.encode()).digest()


def encrypt(text: str) -> str:
    key = _derive_key()
    data = text.encode()

    encrypted_bytes = bytearray()
    for i in range(len(data)):
        encrypted_bytes.append(data[i] ^ key[i % len(key)])

    return base64.b64encode(encrypted_bytes).decode()


def decrypt(token: str) -> str:
    key = _derive_key()
    encrypted_bytes = base64.b64decode(token)

    decrypted_bytes = bytearray()
    for i in range(len(encrypted_bytes)):
        decrypted_bytes.append(encrypted_bytes[i] ^ key[i % len(key)])

    return decrypted_bytes.decode()

def encrypt_log_entry(text):
    return encrypt(text)
def key_health_check():
    return SECRET_KEY is not None and len(SECRET_KEY) > 10


