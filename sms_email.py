import smtplib
from email.message import EmailMessage
from datetime import datetime
from gsecrets import *

# Get the current date and time
now = datetime.now()
# Format the date and time as a string
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

basic_alert_subject = "VIGIL ALERT!! [v012]"

alert_message = "ALERT-WEAPON DETECTED"

sample_alert_message = f"""
!!ALERT!! WEAPON DETECTED
=======================
ADDRESS:
1521 North Highland Ave.,
Los Angeles, CA 90028
LOCATION:
SE entrance
(school auditorium)

DESCRIP: 
black hoodie, backpack
WEAPON-TYPE: 
assault rifle

MAPLINK:
https://www.google.com/maps/search/?api=1&query=34.098248,-118.340965

GEOSTAMP:
34.098248, -118.340965
TIMESTAMP:
{date_time_str}
VIGIL:
HWOOD_HS_LA.8693
"""


def loginSendQuit(server, to_email, msg):
    # server.esmtp_features['auth'] = 'LOGIN PLAIN'
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, to_email, msg.as_string())
    server.quit()

def send_email(to_email, subject, message, override=False):
    try:
        msg = EmailMessage()
        msg["From"] = smtp_username
        msg["To"] = to_email
        msg["Subject"] = subject

        body = message
        # (
        #     f" {message.author.global_name}:.\n"
        #     f"Jump to message {message.jump_url}\n"
        #     f"{message.content}"
        # )
        msg.add_header("Content-Type", "text/plain")
        msg.set_payload(body)
        if smtp_ssl ^ override:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.set_debuglevel(True)
                server.starttls()
                loginSendQuit(server, to_email, msg)
        else:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                #server.set_debuglevel(True)
                loginSendQuit(server, to_email, msg)

        print(f"Email sent successfully to {to_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")

# SMS email gateway : number@server, subject, message
send_email(smtp_phonealias, basic_alert_subject, sample_alert_message)