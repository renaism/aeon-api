import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", default="").split(",")


class DBConfig:
    HOST = os.getenv("DB_HOST", default="127.0.0.1:27017")
    NAME = os.getenv("DB_NAME")
    USERNAME = os.getenv("DB_USERNAME")
    PASSWORD = os.getenv("DB_PASSWORD")