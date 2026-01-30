from dotenv import load_dotenv
import os

load_dotenv()  # <-- THIS is the missing piece

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")
