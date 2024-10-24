import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

import cv2
import torch
# from PIL import Image, ImageDraw, ImageFont
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
import numpy as np

from _gsecrets import *
from _localconfig import *
import launch
import img_proc
# import sms_email 

YELLOW = "\033[33m"
RESET = "\033[0m"  # Resets all formatting

# Load the variables from .env
load_dotenv()

# Suppress macOS specific IMK warnings
sys.stderr = open(os.devnull, 'w')


# print the startupscreen, 
# and ask the user what objects to recognize
searchtext, labels = launch.start_vigil()

# cue up the AI monster
print("\nPlease wait,\n>>> LOADING NEURAL NET...")
processor = AutoProcessor.from_pretrained(img_proc.model_id)
model = AutoModelForZeroShotObjectDetection.from_pretrained(img_proc.model_id).to(img_proc.device)

print(f"{YELLOW}    MODEL LOADED INTO MEMORY{RESET}")

# record the start time
now = datetime.now()

# set the camera stream
print("\n>>> ACCESSING RTSP VIDEO STREAM...")
rtsp_url = f"rtsp://{reolink_rtsp_username}:{reolink_rtsp_pw}@{reolink_rtsp_ip}:{reolink_rtsp_port}/{reolink_rtsp_streamdir}"
print("    cam: " + reolink_mfg + " " + reolink_model)
print("    camIP: " + reolink_rtsp_ip + ":" + reolink_rtsp_port)

# Create a VideoCapture object
# alt-DEBUG : force FFMPEG lib
# cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
rtsp_url_buffed = rtsp_url + "?rtsp_transport=udp&timeout=5000000&buffer_size=8192&max_delay=500000"
# cap = cv2.VideoCapture(rtsp_url_buffed)

# cap = cv2.VideoCapture(rtsp_url)
import vcapture
cap = vcapture.VideoCapture(rtsp_url)

print(f"{YELLOW}    CAMERA STREAM ACQUIRED{RESET}")

# Increase the timeout using FFmpeg options (timeout in microseconds)
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)  # Buffer size 0 to avoid buffer overflows (optional)

# sms_email.send_alert(smtp_phonealias, sms_email.basic_launch_subject, sms_email.launch_message)
launchtime= datetime.now()

while cap.isOpened():
    # Capture the latest frame
    # and begin processing, 
    
    # show elapsed time since last AI run
    prevtime = now
    now = datetime.now()
    protime = now - prevtime
    uptime = now - launchtime
    uptime_sec = int(uptime.total_seconds())
    uhours, remainder = divmod(uptime_sec, 3600)
    uminutes, useconds = divmod(remainder, 60)
    
    formatted_uptime = f"{uhours:02}h{uminutes:02}m{useconds:02}s"

    ftime = now.strftime("%Y-%m-%d %H:%M:%S")
    dtime = "{:.3f} sec".format(protime.total_seconds())

    print("\n>>> DSKY.AI VISION ALGORITHM RUNNING...") 
    print("    FRAME : " + ftime + " (" + dtime +")")
    print("    UPTIME : " + formatted_uptime)
    # Skip frames until only the most recent one is available
    # while cap.grab():
    #     print(cap.get(cv2.CAP_PROP_POS_MSEC))
    #     prevtime = now
    #     now = datetime.now()
    #     if (prevtime - now).seconds > 0.1:
    #         date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    #         print(date_time_str)
    #         continue
    #     else:
    #         print("x", end="", flush=True)
    #         break
    #     pass

    # fc = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # print(fc)
    # continue
    # cap.set(cv2.CAP_PROP_POS_FRAMES, fc)

    # Capture frame-by-frame
    frame = cap.read()

    # if not ret:
    #     print("Error: Could not read frame.")
    #     break

    # Display the resulting frame on-screen
    # -------------------------------------
    # this calls a subroutine from get_grab,
    # which runs CV object recognition algos on the frame
    # and outputs a leblled image with bounding boxes
    # def rtsp_framegrab(processor, model, frame, searchtext):

    image = img_proc.rtsp_framegrab(processor, model, frame, searchtext)
    bgr_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imshow("VIGIL", bgr_image)

    # alt-DEBUG
    # cv2.imshow('RTSP Stream', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()