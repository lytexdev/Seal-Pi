import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', '!@?SuperSecretKey?@!')
    PORT = int(os.getenv('PORT', 5000))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///seal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VIDEO_CAPTURE_DEVICE = int(os.getenv('VIDEO_CAPTURE_DEVICE', 0))