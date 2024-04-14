from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import math
from sort import *
def mission():
    print("Mission starting..............")

#for webcam
cap = cv2.VideoCapture(0)  # For Webcam    0 for 1 webcam
cap.set(3, 1280)                 #Hight
cap.set(4, 780)                 #width

# #for captured video
# cap = cv2.VideoCapture('../Videos/people.mp4') #for vids

model = YOLO('yolov8n.pt')

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]


#tracker
tracker = Sort(max_age=20, min_hits=3 , iou_threshold=0.3) #max_age is for the max frames that can detect, iou is for intersection over union
count = 0

while True:                       #used to turn on the webcam
    success, img = cap.read()
    # print(img.shape)


    results = model(img, stream=True)
    detections = np.empty((0, 5))
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # fancy box by cvzone
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2-x1, y2-y1
            bbox =int(x1), int(y1), int(w), int(h)
        

            #confidence level
            conf = math.ceil((box.conf[0]*100))/100


            #class type
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass == 'person' and conf>0.6:
                count += 1
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))


    resultsTracker = tracker.update(detections)
    print(count)
    if (count == 20):
        mission()
        break

    for result in resultsTracker:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        print(result)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
        cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)), scale=2, thickness=3, offset=10)
        cx, cy = x1 + w // 2, y1 + h // 2


    cv2.imshow("Image", img)
    cv2.waitKey(1)







