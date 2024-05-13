from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import math
from sort import *
import serial
import time
import random

def emulate_gps_data():
    # Define boundaries for Saudi Arabia
    min_lat, max_lat = 16.5, 32.0  # Latitude range
    min_lon, max_lon = 34.5, 55.5  # Longitude range

    # Generate random GPS coordinates within Saudi Arabia
    latitude = random.uniform(min_lat, max_lat)
    longitude = random.uniform(min_lon, max_lon)

    # Return GPS data as a string
    return f"Latitude: {latitude}, Longitude: {longitude}"



def mission():
    gps_data = emulate_gps_data()
    print(gps_data)
    

    # # Define the serial port and baud rate
    # serial_port = 'COM9'  # Update this with your actual serial port
    # baud_rate = 115200  # Make sure to match the baud rate with ESP32-S3

    # # Open the serial port
    # ser = serial.Serial(serial_port, baud_rate, timeout=1)
    # print("Serial port opened successfully")

    # # Send "Hello, world!" to the ESP32-S3
    # ser.write(b"Hello\n")
    # print("Data sent successfully")
    
    # # Wait for a short moment before closing the serial port
    # time.sleep(0.5)
    # ser.close()
    # print("Serial port closed")
    print("Starting Mission............")


model = YOLO('drone.pt')
classNames = ['ignored', 'person', 'boat', 'jetski', 'life_saving_appliances', 'buoy']

#tracker
tracker = Sort(max_age=20, min_hits=3 , iou_threshold=0.3) #max_age is for the max frames that can detect, iou is for intersection over union

           
img = cv2.imread('./2.jpg')  # Read the image
# print(img.shape)


results = model(img)
detections = np.empty((0, 5))
for r in results:
    boxes = r.boxes

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Draw the box with black color

        # Add class name and confidence level
        cls = int(box.cls[0])
        currentClass = classNames[cls]
        conf = math.ceil((box.conf[0]*100))/100
        text = f"{currentClass}: {conf}"
        cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    #confidence level
    conf = math.ceil((box.conf[0]*100))/100


    #class type
    cls = int(box.cls[0])
    print(cls)
    currentClass = classNames[cls]

    if currentClass == 'person':
        mission()

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()