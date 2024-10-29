import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Create Configuration class
class Config:
    SECRET_KEY = os.getenv(key="SECRET_KEY")
    DATABASE_URL = os.getenv(key="DATABASE_URL")
