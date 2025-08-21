import cv2
import time

# RTSP link or CCTV feed URL
camera_url = "rtsp://admin:Admin$1234@192.168.1.104:554/cam/realmonitor?channel=1&subtype=1"

# Output video settings
output_file = "output_high_resolution.mp4"  # Save as MP4 file
fps = 25.0  # Frames per second
resolution = (1920, 1080)  # High resolution (adjust as per your requirement)
duration = 30  # Recording duration in seconds

# Capture the video stream
cap = cv2.VideoCapture(camera_url)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Set resolution (optional, may depend on the camera's capabilities)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
out = cv2.VideoWriter(output_file, fourcc, fps, resolution)

start_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame.")
        break
    
    # Write frame to video file
    out.write(frame)
    
    # Display the frame (optional)
    cv2.imshow('Recording', frame)
    
    # Break after the specified duration
    if time.time() - start_time > duration:
        break
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video saved as {output_file}")
