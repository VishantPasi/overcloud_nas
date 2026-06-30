from pathlib import Path
from config import UPLOAD_FOLDER

# Create uploads folder
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)


def create_user_folder(uid: str):
    """
    Creates a folder for the user if it doesn't exist.
    """

    folder = Path(UPLOAD_FOLDER) / uid

    folder.mkdir(parents=True, exist_ok=True)

    return folder