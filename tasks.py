import os
import cv2
from insightface.app import FaceAnalysis
from mtcnn import MTCNN
import uuid
import json
import numpy as np
import requests
from celery import Celery

app = Celery(
    "tasks",
    broker="amqp://user:password@localhost:5672//",
    backend="redis://localhost:6379/0"
)


# app.conf.worker_pool = 'solo'
# app.conf.worker_pool = 'prefork'

def post_result(data):
    url = "http://localhost:8001/api/embedding"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.qQQQlF_Ex3zyHSIsZarRQJZGdQOsB-FOgPrPnL1F7Vc"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def augment_face(uid: str):
    return ""


def extract_face(uid: str):
    directory = f"uploads/{uid}"
    face_directory = f"uploads/{uid}/faces"
    # Prepare
    if not os.path.exists(face_directory):
        os.makedirs(face_directory, exist_ok=True)

    # List files
    files = os.listdir(directory)
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    detector = MTCNN()
    padding = [50, 50]
    result = []
    for file in files:
        image = cv2.imread(os.path.join(directory, file))
        faces = detector.detect_faces(image)

        for face in faces:
            x, y, w, h = face['box']
            face_image = image[y - padding[1]:y + h + padding[1], x - padding[0]:x + w + padding[0]]

            face_filename = f"{face_directory}/{uuid.uuid4()}.jpg"
            cv2.imwrite(face_filename, face_image)
            result.append((x, y, w, h))

    return result


def calc_embedding(uid: str):
    directory = f"uploads/{uid}/faces"
    # directory = f"uploads/{uid}"
    files = os.listdir(directory)
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]

    arc_face_app = FaceAnalysis()
    arc_face_app.prepare(ctx_id=0, det_size=(640, 640))
    print(os.path.join(directory, files[0]))

    embeddings = []
    for file in files:
        img = cv2.imread(os.path.join(directory, file))
        faces = arc_face_app.get(img)

        if faces and len(faces) > 0:
            embedding = faces[0].normed_embedding
            embeddings.append(embedding)
        else:
            print("No face detected")

    best_embedding = np.mean(embeddings, axis=0)
    return best_embedding.tolist()


@app.task
def add_task(uid):
    extract_face(uid)
    emd = calc_embedding(uid)

    data_string = {
        "embedding": emd,
        "uid": uid
    }

    r = post_result(data_string)
    return r
