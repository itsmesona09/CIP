#AURA - Attendance with Unique Recognition and Audio

import cv2
import threading
from deepface import DeepFace
import speech_recognition as sr
import datetime
import json
import signal
import sys

teacher_verified = True
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

reference_img = cv2.imread("teacher.jpg")
attendance = {}
listening = False
lock = threading.Lock()

def verify_teacher_face(frame):
    global teacher_verified
    try:
        result = DeepFace.verify(frame, reference_img.copy())
        teacher_verified = result['verified']
    except:
        teacher_verified = False

def listen_for_students():
    global listening
    listening = True
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("MARKING ATTENDANCE!")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print("NAME HEARD", command)

            if "present mam" in command:
                name = command.replace("present mam", "").strip().title()
                if not name:
                    name = "Unknown Student"
                mark_attendance(name)

    except Exception as e:
        print("Error in speech recognition:", e)
    finally:
        listening = False

def mark_attendance(name):
    with lock:
        if name and name not in attendance:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            attendance[name] = now
            print(f"{name} marked present at {now}")
            save_attendance()

def save_attendance():
    with open("attendance.json", "w") as f:
        json.dump(attendance, f, indent=4)

def graceful_exit(signum, frame):
    print("\n[INFO] ATTENDANCE CLOSED!")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

frame_counter = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if not teacher_verified and frame_counter % 30 == 0:
        threading.Thread(target=verify_teacher_face, args=(frame.copy(),)).start()

    if teacher_verified:
        cv2.putText(frame, "WELCOME TEACHER!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if not listening:
            threading.Thread(target=listen_for_students).start()
    else:
        cv2.putText(frame, "SCANNING FOR TEACHERS' FACE!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("AURA", frame)

    if cv2.waitKey(1) == ord('q'):
        break
    frame_counter += 1

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)
cap.release()
cv2.destroyAllWindows()