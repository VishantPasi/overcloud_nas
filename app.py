from fastapi import Body, FastAPI, HTTPException, UploadFile, File, Form
import aiofiles
from pathlib import Path
import shutil

from fastapi.responses import FileResponse

from config import UPLOAD_FOLDER
from storage import create_user_folder

app = FastAPI(
    title="Hybrid NAS"
)


@app.get("/")
async def home():
    return {"message": "Hybrid NAS Server Running"}


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

@app.delete("/deleteFolder")
async def delete_folder(data: dict = Body(...)):
    uid: str = data["uid"]
    folderId: str = data["folderId"]

    user_folder = create_user_folder(uid)

    folder_path = user_folder / folderId

    if not folder_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Folder not found"
        )

    if not folder_path.is_dir():
        raise HTTPException(
            status_code=400,
            detail="Specified path is not a folder"
        )

    shutil.rmtree(folder_path)

    return {
        "success": True,
        "message": "Folder deleted successfully",
        "folderId": folderId
    }


@app.post("/upload")
async def upload_file(
    uid: str = Form(...),
    folderId: str = Form(...),
    fileId: str = Form(...),
    file: UploadFile = File(...)
): 
     # Create the user's folder
    user_folder = create_user_folder(uid)

    # Destination path
    file_path = user_folder / folderId / fileId

    # Save file in 1 MB chunks
    async with aiofiles.open(file_path, "wb") as buffer:

        while chunk := await file.read(1024 * 1024):
            await buffer.write(chunk)

    return {
        "success": True,
        "filename": file.filename,
        "uid": uid
    }


@app.get("/download")
async def download_file(
    uid: str,
    folderId: str,
    fileId: str,
):
    user_folder = create_user_folder(uid)

    file_path = user_folder / folderId / fileId

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=file_path,
        filename=fileId,
        media_type="application/octet-stream",
    )


@app.delete("/delete")
async def delete_file(data: dict = Body(...)):
    uid: str = data["uid"]
    folderId: str = data["folderId"]
    fileId: str = data["fileId"]


    user_folder = create_user_folder(uid)

    file_path = user_folder / folderId / fileId

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=400,
            detail="Specified path is not a file"
        )

    file_path.unlink()

    return {
        "success": True,
        "message": "File deleted successfully",
        "fileId": fileId
    }