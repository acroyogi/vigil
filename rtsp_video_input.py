import cv2

# RTSP stream URL of the camera
rtsp_url = "rtsp://your_camera_ip_address"

# Open video stream
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break
    
    # Display the frame (for debugging, can be removed for production)
    cv2.imshow('RTSP Stream', frame)

    # Exit with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
