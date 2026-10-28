import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(to_email, subject, body):
    """
    Robust Gmail SMTP sender supporting both Port 587 (STARTTLS) and Port 465 (SSL)
    """
    if os.getenv("SEND_EMAIL", "false").lower() not in ("true", "1", "yes"):
        print("ℹ Email notifications are disabled in environment.")
        return True  # Return True so SOS doesn't break if email is intentionally toggled off

    host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    port = int(os.getenv("EMAIL_PORT", 587))
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not user or not password:
        print(" Email credentials missing in .env file.")
        return False

    try:
        print(f" Connecting to Gmail SMTP ({host}:{port})...")
        
        # Handle port-specific connection security
        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=10)
        else:
            server = smtplib.SMTP(host, port, timeout=10)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(user, password)

        # Build message
        msg = MIMEMultipart()
        msg["From"] = user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.sendmail(user, to_email, msg.as_string())
        server.quit()
        print(" Emergency SOS Email sent successfully!")
        return True

    except Exception as e:
        print(f" Email failed: {str(e)}")
        return False