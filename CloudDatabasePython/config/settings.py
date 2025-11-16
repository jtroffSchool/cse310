import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Firestore service account (set GOOGLE_APPLICATION_CREDENTIALS env var)
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Optional: Firebase/GCP project ID
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
