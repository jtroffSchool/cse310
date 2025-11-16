from google.cloud.firestore import SERVER_TIMESTAMP
from .firestore_client import get_db

db = get_db()

def run_monthly_rollover():
    """
    For every user:
      lastMonthTotal = currentMonthTotal
      currentMonthTotal = 0
      averageTime = 0
      (optionally) currentRank = 0
    """
    users_ref = db.collection("users")
    users = users_ref.stream()

    count = 0
    for doc in users:
        data = doc.to_dict() or {}
        current_total = data.get("currentMonthTotal", 0)

        print(f"Rolling over user {doc.id}: currentMonthTotal={current_total}")

        doc.reference.set({
            "lastMonthTotal": current_total,
            "currentMonthTotal": 0,
            "averageTime": 0,
            "currentRank": 0,
            "updatedAt": SERVER_TIMESTAMP
        }, merge=True)

        count += 1

    print(f"Monthly rollover complete for {count} users.")
