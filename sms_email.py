import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from PIL import Image
import io

from datetime import datetime
from _gsecrets import *



# Get the current date and time
now = datetime.now()
# Format the date and time as a string
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

tYELLOW = "\033[33m"
tRESET = "\033[0m"  # Resets all formatting

basic_launch_subject = f"VIGIL ACTIVE [v{g_version}]"
basic_alert_subject = f"VIGIL ALERT!! [v{g_version}]"
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
1521 North Highland Ave.
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



# Compress and prepare the image
def compress_image(pil_image, quality=70):
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='JPEG', quality=quality)
    img_byte_arr.seek(0)
    return img_byte_arr



# Upload the image to your web server via FTP
def upload_image_to_ftp(ftp_host, ftp_user, ftp_pass, remote_path, pil_image):
    # Compress the image to JPEG
    img_byte_arr = compress_image(pil_image)

    # Connect to the FTP server
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_pass)

    # Upload the image to the specified path on the server
    ftp.storbinary(f'STOR {remote_path}', img_byte_arr)

    # Close the connection
    ftp.quit()
    print(f"Image successfully uploaded to {ftp_host}/{remote_path}")



# Send email with image attachment
def send_email_with_image(to_email, subject, message_text, pil_image, override=False):
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the text message
        msg.attach(MIMEText(message_text, 'plain'))

        # Compress the image and get the byte stream
        img_byte_arr = compress_image(pil_image)

        # Attach the image as a MIMEImage object
        image_mime = MIMEImage(img_byte_arr.getvalue(), _subtype="jpeg", name="compressed_image.jpg")
        msg.attach(image_mime)

        try:
            # Use smtplib to send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, to_email, msg.as_string())  # Correct: msg.as_string()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

        # msg.add_header("Content-Type", "multipart/mixed")
        # msg.set_payload("test")

        # if smtp_ssl ^ override:
        #     with smtplib.SMTP(smtp_server, smtp_port) as server:
        #         server.set_debuglevel(True)
        #         server.starttls()
        #         loginSendQuit(server, to_email, msg.as_string())
        # else:
        #     with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        #         #server.set_debuglevel(True)
        #         loginSendQuit(server, to_email, msg.as_string())

        print(f"\n+++ SCREENGRAB transmitted:\n{tYELLOW}    {alert_user} @ {alert_phone}{tRESET}")

    except Exception as e:
        print(f"Failed to send IMAGE : {e}")


