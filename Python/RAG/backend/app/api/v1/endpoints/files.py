from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import os
import shutil
from app.helpers.embeding.embeding import initialize_vector_store

router = APIRouter(prefix="/files", tags=["files"])

# Todo: seperate this code later from the api to a new .py file
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
@router.post("/upload")
async def create_upload_files(files: list[UploadFile]):
    saved_files = []
    for file in files:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)
    # trigger every time when a file is saved
    await initialize_vector_store()
    return {"saved_files": saved_files}


@router.get("/list")
async def list_files():
    # .iterdir() is the modern way to list files with Pathlib
    # filter using .is_file() to ensure don't return sub-folders
    files = [f.name for f in UPLOAD_DIR.iterdir() if f.is_file()]
    return {"files": files}



# *testing
# @router.post("/upload")
# async def create_upload_files(files: list[UploadFile]):
#     return {"filename":[file.filename for file in files]}