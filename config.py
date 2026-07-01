from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

UPLOAD_FOLDER = Path(os.getenv("UPLOAD_FOLDER", "uploads"))
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))