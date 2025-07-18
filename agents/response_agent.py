import smtplib
from email.mime.text import MIMEText

def send_confirmation_email(to_email, status, reason="", user_name=""):
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
        print("Email Error:", str(e))