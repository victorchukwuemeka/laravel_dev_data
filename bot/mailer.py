import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(to_email, github_username):
    msg = EmailMessage()
    msg["Subject"] = "Hello aquapush"
    msg["From"] = "toyinsan27@gmail.com"
    msg["To"] = to_email
    msg.set_content(f"""
Hi {github_username},

I’m reaching out to introduce AquaPush — a platform that makes deploying Laravel apps to DigitalOcean **super easy**.

All you need to do is provide your SSH key and DigitalOcean API key, and your deployment is handled automatically. No fuss, no headaches.

Check it out here: https://aquapush.dev

Give it a try and deploy your apps with ease!

— Oluwatoyin Sangotade
Marketing @ AquaPush
""")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        user = os.getenv("EMAIL_USER")
        password  = os.getenv("EMAIL_PASS")
        if not user or not password:
            raise ValueError("the evn variable is not set")
        smtp.login(user,password)
        smtp.send_message(msg)

    return True
