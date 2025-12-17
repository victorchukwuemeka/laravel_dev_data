import os

def send_email(to_email, github_username):
    
    content = f"""
To: {to_email}
Hi {github_username},

Just reaching out to share Laraub — a platform for Laravel developers
to discover and share useful packages.

No pressure at all.
Have a great day!

— Victor
"""

    
    os.makedirs("test/emails", exist_ok=True)
    
    
    filename = f"test/emails/email_to_{github_username}.txt"
    with open(filename, "w") as f:
        f.write(content)

    print(f"📄 Email written to {filename} (simulated as text)")
    return True
