import os
from dotenv import load_dotenv
from google.cloud import firestore

# Load environment variables from .env
load_dotenv()

# Get the service account JSON path from environment variable
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

if not SERVICE_ACCOUNT_FILE:
    raise ValueError(
        "GOOGLE_APPLICATION_CREDENTIALS not set in environment or .env file"
    )

if not PROJECT_ID:
    raise ValueError(
        "GOOGLE_CLOUD_PROJECT not set in environment or .env file"
    )

# Optional: print to verify
print("Using service account:", SERVICE_ACCOUNT_FILE)
print("Firestore project:", PROJECT_ID)

def get_db():
    """
    Returns a Firestore client using the service account.
    """
    return firestore.Client.from_service_account_json(
        SERVICE_ACCOUNT_FILE,
        project=PROJECT_ID
    )
