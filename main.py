import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import cv2
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
import numpy as np

from gsecrets import *
import launch
import get_grab
 
 
# Load the variables from .env
load_dotenv()

# print the startupscreen, 
# and ask the user what objects to recognize
searchtext, labels = launch.start_vigil()

# cue up the AI monster
print("\nPlease wait,\n>>> LOADING NEURAL NET...")
processor = AutoProcessor.from_pretrained(get_grab.model_id)
model = AutoModelForZeroShotObjectDetection.from_pretrained(get_grab.model_id).to(get_grab.device)

# record the start time
now = datetime.now()

# set the camera stream
print("\n>>> ACCESSING RTSP VIDEO STREAM...")
rtsp_url = f"rtsp://{reolink_rtsp_username}:{reolink_rtsp_pw}@{reolink_rtsp_ip}:{reolink_rtsp_port}"
print("    camIP: " + reolink_rtsp_ip + ":" + reolink_rtsp_port)

# Create a VideoCapture object
# alt-DEBUG : force FFMPEG lib
# cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

cap = cv2.VideoCapture(rtsp_url)
print("    CAMERA STREAM ACQUIRED")


if not cap.isOpened():
    print("Error: Could not open video stream.")
else:
    while True:
        # Capture the latest frame
        # and begin processing, 
        
        # show elapsed time since last AI run
        prevtime = now
        now = datetime.now()
        protime = now - prevtime

        ftime = now.strftime("%Y-%m-%d %H:%M:%S")
        dtime = "{:.3f} sec".format(protime.total_seconds())

        print("\n>>> DSKY.AI VISION ALGORITHM RUNNING...") 
        print("    FRAME : " + ftime)
        print("    tDELTA : " + dtime)

        # Skip frames until only the most recent one is available
        # while cap.grab():
        #     prevtime = now
        #     now = datetime.now()
        #     if prevtime - now > timedelta(seconds=1):
        #         date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        #         print(date_time_str)
        #     else:
        #         print("x",end="", flush=True)
        #         break
        #     pass

        fc = cap.get(cv2.CAP_PROP_FRAME_COUNT)-1
        cap.set(cv2.CAP_PROP_POS_FRAMES, fc)

        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Display the resulting frame on-screen
        # -------------------------------------
        # this calls a subroutine from get_grab,
        # which runs CV object recognition algos on the frame
        # and outputs a leblled image with bounding boxes
        # def rtsp_framegrab(processor, model, frame, searchtext):

        image = get_grab.rtsp_framegrab(processor, model, frame, searchtext)

        #alt-DEBUG
        # cv2.imshow('RTSP Stream', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()