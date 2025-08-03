import smtplib
from email.mime.text import MIMEText
from openai import OpenAI
import os

'''def send_confirmation_email(to_email, status, reason="", user_name=""):
    try:
        #body = generate_email_body(status, reason, user_name)
        body = "Your KYC validation is: {status.upper()}"
        msg = MIMEText(body)
        msg['Subject'] = 'KYC Validation Result'
        msg['From'] = 'noreply@example.com'
        msg['To'] = to_email

        server = smtplib.SMTP('localhost')
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email Error:", str(e))'''



client = OpenAI()

def generate_email_body(status: str, reason: str = "", user_name: str = "") -> str:
    status_msg = "approved" if status == "success" else "rejected"
    prompt = f"""
    Compose a polite and professional email message to a user named '{user_name}'.
    The email should inform them that their KYC validation was {status_msg}.
    {"Include the reason: " + reason if reason else ""}
    Keep it concise and friendly.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an email assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.5
    )
    return completion.choices[0].message.content

def send_confirmation_email(to_email, status, reason="", user_name=""):
    try:
        body = generate_email_body(status, reason, user_name)
        msg = MIMEText(body)
        msg['Subject'] = 'KYC Validation Result'
        msg['From'] = 'noreply@example.com'
        msg['To'] = to_email

        server = smtplib.SMTP('localhost',1025)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email Error:", str(e))

