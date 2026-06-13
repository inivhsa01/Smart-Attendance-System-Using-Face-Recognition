import cv2
import os
import pandas as pd
from datetime import datetime
import pickle

ATTENDANCE_FILE = "attendance.xlsx"
DATASET_PATH = "dataset"
MODEL_FILE = "trainer.yml"
LABELS_FILE = "labels.pkl"

if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)

# ================= MARK ATTENDANCE =================
def mark_attendance(name, roll):

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    new = pd.DataFrame([[name, roll, date, time_now, "Present"]],
                       columns=["Name", "Roll", "Date", "Time", "Status"])

    if os.path.exists(ATTENDANCE_FILE):
        old = pd.read_excel(ATTENDANCE_FILE)

        if ((old["Name"] == name) & (old["Date"] == date)).any():
            return f"{name} Already Marked Today"

        updated = pd.concat([old, new], ignore_index=True)
        updated.to_excel(ATTENDANCE_FILE, index=False)
    else:
        new.to_excel(ATTENDANCE_FILE, index=False)

    return f"{name} Marked ✔"


# ================= ADD STUDENT =================
def add_student(name, roll):

    folder = os.path.join(DATASET_PATH, f"{name}_{roll}")

    if not os.path.exists(folder):
        os.makedirs(folder)

    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Add Student (Press Q)", frame)

        cv2.imwrite(f"{folder}/{count}.jpg", frame)
        count += 1

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 25:
            break

    cap.release()
    cv2.destroyAllWindows()

    return f"Student Added ✔ {name}"


# ================= LOAD MODEL =================
def load_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_FILE)

    with open(LABELS_FILE, "rb") as f:
        labels = pickle.load(f)

    return recognizer, {v: k for k, v in labels.items()}


# ================= CAMERA (INSTANT CLOSE AFTER DETECTION) =================
def start_camera():

    if not os.path.exists(MODEL_FILE):
        return "Model Not Trained"

    recognizer, labels = load_model()

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)

    message = "No Face Detected"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        cv2.imshow("Smart Attendance System", frame)

        for (x, y, w, h) in faces:

            roi = gray[y:y+h, x:x+w]

            try:
                id_, conf = recognizer.predict(roi)

                if conf < 70:
                    name = labels[id_]
                    roll = "101"
                else:
                    name = "Unknown"
                    roll = "000"

            except:
                name = "Unknown"
                roll = "000"

            if name != "Unknown":
                message = mark_attendance(name, roll)

                cv2.putText(frame, "MARKED ✔", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                cv2.imshow("Smart Attendance System", frame)
                cv2.waitKey(400)

                cap.release()
                cv2.destroyAllWindows()

                return message

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(frame, "Unknown", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return message