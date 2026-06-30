from fastapi import FastAPI, UploadFile, File, Form
import aiofiles
from pathlib import Path

from storage import create_user_folder

app = FastAPI(
    title="Hybrid NAS"
)


@app.get("/")
async def home():
    return {"message": "Hybrid NAS Server Running"}


@app.post("/upload")
async def upload_file(
    uid: str = Form(...),
    file: UploadFile = File(...)
): 
     # Create the user's folder
    user_folder = create_user_folder(uid)

    # Destination path
    file_path = user_folder / file.filename

    # Save file in 1 MB chunks
    async with aiofiles.open(file_path, "wb") as buffer:

        while chunk := await file.read(1024 * 1024):
            await buffer.write(chunk)

    return {
        "success": True,
        "filename": file.filename,
        "uid": uid
    }