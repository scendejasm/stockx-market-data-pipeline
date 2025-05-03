import os
from dotenv import load_dotenv

load_dotenv() # Loads from .env in root

EBAY_APP_ID = os.getenv("EBAY_APP_ID")

if not EBAY_APP_ID:
    raise ValueError("Missing EBAY_APP_ID in environment variables")
