import os
from dotenv import load_dotenv

load_dotenv()  # read .env file

DB_PATH = os.getenv("DB_PATH", "sqlite:///./ecom.db")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("Please set GROQ_API_KEY in .env")
