from pathlib import Path
from fastapi import UploadFile, HTTPException

from typing import List
import uuid
import shutil

UPLOAD_DIR = "uploads"
ALLOWED_FILE_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

root_path = Path(UPLOAD_DIR)
root_path.mkdir(parents=True, exist_ok=True)

async def upload(files: List[UploadFile], uid: str, subfolder: str):
    saved_files = []

    # Validate files first
    if len(files) > 3:
        raise HTTPException(status_code=400, detail="Just 3 images")

    for file in files:
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(status_code=400, detail="invalid file type")

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, detail="File size is exceeded")

    #  prepare folder
    user_folder = root_path / uid / subfolder
    shutil.rmtree(user_folder, ignore_errors=True)
    user_folder.mkdir(parents=True, exist_ok=True)

    # Loop over to upload
    for file in files:
        file_ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_location = user_folder / filename
        print(file_location)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append(
            {"filename": file.filename, "saved_path": file_location})
