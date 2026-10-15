import os
from dotenv import load_dotenv

load_dotenv()

_testing = bool(os.environ.get("TESTING"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///test_accessevent.db" if _testing
        else os.environ.get("DATABASE_URL", "sqlite:///accessevent.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_HOURS = 24
