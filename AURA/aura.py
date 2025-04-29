import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import json

path = 'Images_Attendance'
attendance_file = 'attendance.json'

images = []
classNames = []

myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name, date_today):
    if os.path.exists(attendance_file):
        try:
            with open(attendance_file, 'r') as f:
                attendance_data = json.load(f)
        except json.JSONDecodeError:
            attendance_data = {}
    else:
        attendance_data = {}

    if date_today not in attendance_data:
        attendance_data[date_today] = []

    if name not in attendance_data[date_today]:
        attendance_data[date_today].append(name)

    with open(attendance_file, 'w') as f:
        json.dump(attendance_data, f, indent=4)

encodeListKnown = findEncodings(images)

cap = cv2.VideoCapture(1)

while True:
    success, img = cap.read()
    if not success:
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS, model="hog")
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    time_now = datetime.now()
    date_today = time_now.strftime('%d/%m/%Y')

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 250, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            markAttendance(name, date_today)

    cv2.imshow('webcam', img)

    if cv2.waitKey(10) == 13:
        break

cap.release()
cv2.destroyAllWindows()
