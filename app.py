from fastapi import Body, FastAPI, HTTPException, UploadFile, File, Form
import aiofiles
from pathlib import Path

from config import UPLOAD_FOLDER
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

@app.post("/createFolder")
async def create_folder(data: dict = Body(...)):
    uid = data["uid"]
    folderName = data["folderName"]

    user_folder = UPLOAD_FOLDER / uid
    user_folder.mkdir(parents=True, exist_ok=True)

    folder_path = user_folder / folderName

    if folder_path.exists():
        raise HTTPException(
            status_code=409,
            detail="Folder already exists"
        )

    folder_path.mkdir()

    return {
        "success": True,
        "message": "Folder created successfully",
        "path": str(folder_path)
    }