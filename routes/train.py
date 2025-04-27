from fastapi import APIRouter, UploadFile, File, Form

from controllers import update_face, compare_face
from tasks import app as ceapp

router = APIRouter()

@router.post("/train")
async def train_model(uid: str = Form(...), files: list[UploadFile] = File(...)):
    return await update_face.update_face(files, uid)

@router.post("/test")
async def test_model(uid: str = Form(...), files: list[UploadFile] = File(...)):
    return await compare_face.compare_face(files, uid)

@router.get("/task/{task_id}")
def get_task_status(task_id: str):
    result = ceapp.AsyncResult(task_id)
    if result.ready():
        return {"task_id": task_id, "status": result.status, "result": result.result}
    else:
        return {"task_id": task_id, "status": result.status, "result": "Task is still processing"}