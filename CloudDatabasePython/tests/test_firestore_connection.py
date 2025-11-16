from google.cloud import firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for service account path
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

print(f"Using service account: {cred_path}")

# Initialize Firestore client
db = firestore.Client()

# List all collections
print("Collections in your project:")
for col in db.collections():
    print("-", col.id)

# Write a test document
test_ref = db.collection("test_connection").document("ping")
test_ref.set({"message": "Hello Firestore!"})
print("Wrote test document to 'test_connection/ping'.")

# Read it back
doc = test_ref.get()
if doc.exists:
    print("Read back document:", doc.to_dict())
else:
    print("Failed to read test document.")
