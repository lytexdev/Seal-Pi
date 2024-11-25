import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Set Seal-Pi configuration from .env file."""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', '!@?Sup€rS€cretK€y?@!')
    PORT = int(os.getenv('PORT', 5000))
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    LOCKOUT_DURATION_MINUTES = int(os.getenv('LOCKOUT_DURATION_MINUTES', 20))
    VIDEO_CAPTURE_DEVICE = int(os.getenv('VIDEO_CAPTURE_DEVICE', 0))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    IP_BLACKLIST = os.getenv("IP_BLACKLIST", "").split(",") if os.getenv("IP_BLACKLIST") else []

    SQLALCHEMY_DATABASE_URI = 'sqlite:///seal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER_TOKEN = os.getenv('SERVER_TOKEN', 'secure_server_token')