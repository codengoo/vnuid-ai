import asyncio
from typing import List

from fastapi import UploadFile

from services import uploader
from tasks import app as ceapp

async def update_face(files: List[UploadFile], uid: str):
    await uploader.upload(files, uid, "train")

    # Add train task
    task = ceapp.send_task("tasks.update_face", args=[uid])

    return {"task_id": task.id}
