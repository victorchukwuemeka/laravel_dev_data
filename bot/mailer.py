import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(to_email, github_username):
    msg = EmailMessage()
    msg["Subject"] = "Hello laraub"
    msg["From"] = "chukwuemekavictor693@gmail.com"
    msg["To"] = to_email
    msg.set_content(f"""
Hi {github_username},

Just reaching out to share Laraub — a platform for Laravel developers
to discover and share useful packages.

No pressure at all.
Have a great day!

— Victor
""")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        user = os.getenv("EMAIL_USER")
        password  = os.getenv("EMAIL_PASS")
        if not user or not password:
            raise ValueError("the evn variable is not set")
        smtp.login(user,password)
        smtp.send_message(msg)

    return True
