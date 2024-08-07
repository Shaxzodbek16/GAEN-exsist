import smtplib
from email.mime.text import MIMEText


def send_email(sender_email: str, sender_email_password: str, to_email: str, message: str) -> bool:
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_email_password)
            msg = MIMEText(message, 'plain')
            msg['Subject'] = "GAEN"
            msg['From'] = sender_email
            msg['To'] = to_email
            server.sendmail(sender_email, to_email, msg.as_string())
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    sender_email = "muxtorovshaxzodbek16@gmail.com"
    sender_email_password = "xuoz qigk ipia wifm"
    to_email = "abroyevmuslimbek@gmail.com"
    message = '123456'
    print(send_email(sender_email, sender_email_password, to_email, message))
