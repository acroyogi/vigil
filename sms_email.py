import smtplib
from email.message import EmailMessage
from datetime import datetime
from _gsecrets import *

# Get the current date and time
now = datetime.now()
# Format the date and time as a string
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

tYELLOW = "\033[33m"
tRESET = "\033[0m"  # Resets all formatting


basic_launch_subject = "VIGIL ACTIVE [v015]"
basic_alert_subject = "VIGIL ALERT!! [v015]"

alert_message = "ALERT-WEAPON DETECTED"

launch_message = f"""
VIGIL PERIMETER SECURITY
=======================
SYSTEM ACTIVATED
{date_time_str}
"""


sample_alert_message = f"""
!!ALERT!! WEAPON DETECTED
=======================
ADDRESS:
1521 North Highland Ave.,
Los Angeles, CA 90028

LOC: SE entrance
(school auditorium)

DESCRIP: 
black hoodie, backpack
WEAPON-TYPE: 
assault rifle

MAPLINK:
https://www.google.com/maps/search/?api=1&query=34.098248,-118.340965

TIMESTAMP:
{date_time_str}
VIGIL_ID:
HWOOD_HS_LA.8693
"""

# GEOSTAMP:
# 34.098248, -118.340965


def loginSendQuit(server, to_email, msg):
    # server.esmtp_features['auth'] = 'LOGIN PLAIN'
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, to_email, msg.as_string())
    server.quit()

def send_alert(to_email, subject, message, override=False):
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

        print(f"\n+++ SMS successfully transmitted:\n{tYELLOW}    {alert_user} @ {alert_phone}{tRESET}")

    except Exception as e:
        print(f"Failed to send : {e}")

# SMS email gateway : number@server, subject, message
