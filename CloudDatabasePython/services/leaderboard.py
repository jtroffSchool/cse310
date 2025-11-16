from google.cloud import firestore
from .firestore_client import get_db

db = get_db()

def get_current_month_leaderboard(limit: int | None = None):
    """
    Returns a list of users sorted by currentMonthTotal (descending),
    with ranks calculated in Python.
    """
    users_ref = db.collection("users")

    # Order by currentMonthTotal descending; missing fields treated as 0 in our code
    query = users_ref.order_by("currentMonthTotal", direction=firestore.Query.DESCENDING)
    if limit:
        query = query.limit(limit)

    docs = query.stream()

    leaderboard = []
    rank = 1

    for doc in docs:
        data = doc.to_dict() or {}
        current_total = data.get("currentMonthTotal", 0)
        last_total = data.get("lastMonthTotal", 0)
        avg_time = data.get("averageTime", 0)
        username = data.get("username", doc.id)

        leaderboard.append({
            "rank": rank,
            "userId": doc.id,
            "username": username,
            "currentMonthTotal": current_total,
            "lastMonthTotal": last_total,
            "averageTime": avg_time,
        })

        rank += 1

    return leaderboard
    