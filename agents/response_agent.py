import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
import os
import streamlit as st

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


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
GMAIL_APP_PWD = st.secrets["GMAIL_APP_PWD"]
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_email_body(status: str, reason: str = "", user_name: str = "") -> str:

    status_msg = "approved" if status == "success" else "rejected"
    prompt = f"""
    Compose a polite and professional email message to a user named '{user_name}'.
    The email should inform them that their KYC validation was {status_msg}.
    {"Include the reason: " + reason if reason else ""}. If the reason says that there is mismatch with database or record in file,
    then mention that data is not matching with Test unique id database. In case status_msg is approved and reason is empty
    no need to mention any reason in the email.
    Keep it concise and professional. The message is sent by KYC Assistant from GENAI UID Project
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

    
    app_password = GMAIL_APP_PWD
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    print("Intended recipient : " + to_email + "for name : " + user_name)
    message["To"] = "souravk.chatterjee@outlook.com"
    message["Subject"] = 'KYC Validation Result'
    body = generate_email_body(status, reason, user_name)
    # Attach text body
    message.attach(MIMEText(body, "plain"))
    try:
        
        """   
            msg = MIMEText(body)
            msg['Subject'] = 'KYC Validation Result'
            msg['From'] = sender_email
            msg['To'] = to_email
        """
        

        """  server = smtplib.SMTP('localhost',1025)
            server.send_message(msg)
        """
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, app_password)
        server.sendmail(SENDER_EMAIL, to_email, message.as_string())
        print("Email sent successfully!")
        server.quit()
    except Exception as e:
        print("Email Error:", str(e))

