import os
from dotenv import load_dotenv

load_dotenv() # Loads from .env in root

EBAY_APP_ID = os.getenv("EBAY_APP_ID")
X_API_KEY = os.getenv("X_API_KEY")

if not EBAY_APP_ID:
    raise ValueError("Missing EBAY_APP_ID in environment variables")
