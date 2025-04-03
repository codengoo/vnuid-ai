from fastapi import APIRouter, UploadFile, File, Form
from services.train_model import upload_images

router = APIRouter()

@router.post("/train")
async def train_model(uid: str = Form(...), files: list[UploadFile] = File(...)):
    print(uid)
    return await upload_images(files, uid)