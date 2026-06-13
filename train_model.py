import cv2
import os
import numpy as np
from PIL import Image
import pickle

DATASET_PATH = "dataset"

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

faces = []
ids = []
labels = {}
current_id = 0

# ---------- LOAD DATASET ----------
for root, dirs, files in os.walk(DATASET_PATH):

    for file in files:
        if file.endswith("jpg"):

            path = os.path.join(root, file)
            label = os.path.basename(root)

            if label not in labels:
                labels[label] = current_id
                current_id += 1

            id_ = labels[label]

            img = Image.open(path).convert("L")
            img_np = np.array(img, "uint8")

            detected = detector.detectMultiScale(img_np)

            for (x, y, w, h) in detected:
                faces.append(img_np[y:y+h, x:x+w])
                ids.append(id_)

# ---------- TRAIN MODEL ----------
recognizer.train(faces, np.array(ids))

# Save model
recognizer.save("trainer.yml")

# Save labels
with open("labels.pkl", "wb") as f:
    pickle.dump(labels, f)

print("Training completed ✔ Model saved!")