import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")