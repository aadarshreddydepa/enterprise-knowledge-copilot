from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings(
    DATABASE_URL=os.getenv("DATABASE_URL"),
    DATABASE_URL_SYNC=os.getenv("DATABASE_URL_SYNC"),
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
)
