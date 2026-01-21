import smtplib
from email.message import EmailMessage

# simple contact mapping
CONTACTS = {
    "me": "your_email@gmail.com"
}

def send_email(to_name, subject, body, speak):
    if to_name not in CONTACTS:
        speak("Contact not found")
        return None

    msg = EmailMessage()
    msg["From"] = "your_email@gmail.com"
    msg["To"] = CONTACTS[to_name]
    msg["Subject"] = subject
    msg.set_content(body)

    return msg
