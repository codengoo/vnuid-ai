import os
import cv2
from insightface.app import FaceAnalysis
from mtcnn import MTCNN
import uuid
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
# app.conf.worker_pool = 'threads'

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


def calc_embedding(directory: str):
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
            print("Detect face")
            embedding = faces[0].normed_embedding
            embeddings.append(embedding)
        else:
            print("No face detected")

    if len(embeddings) > 0:
        best_embedding = np.mean(embeddings, axis=0)
        return best_embedding.tolist()
    raise Exception("No embedding")


@app.task
def compare_face(uid):
    emd1 = calc_embedding(f"uploads/{uid}/train")
    print(emd1)

    emd2 = calc_embedding(f"uploads/{uid}/test")
    print(emd2)

    simp = np.dot(emd1, emd2)
    print(simp)

    return post_result(simp)

@app.task
def update_face(uid):
    # extract_face(f"uploads/{uid}/train")
    emd = calc_embedding(f"uploads/{uid}/train")
    print(emd)

    data_string = {
        "embedding": emd,
        "uid": uid
    }

    return post_result(data_string)