from dotenv import load_dotenv
import os

load_dotenv()

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))