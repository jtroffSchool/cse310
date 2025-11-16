from datetime import datetime
from google.cloud.firestore import SERVER_TIMESTAMP
from .firestore_client import get_db
from .scoring import calculate_daily_score
from .utils import today_id, start_of_month

db = get_db()

def submit_daily_score(
    user_id: str,
    time_seconds: float,
    mistakes: int,
    hints_used: int,
    difficulty: int,
    date_str: str | None = None
):
    """
    Write daily score + raw user inputs into Firestore.
    If date_str is given (YYYY-MM-DD), use that as the document ID.
    Otherwise, use today's date.
    """
    daily_score = calculate_daily_score(time_seconds, mistakes, hints_used, difficulty)

    doc_id = date_str if date_str else today_id()

    doc_ref = (
        db.collection("users")
          .document(user_id)
          .collection("scores")
          .document(doc_id)
    )

    doc_ref.set({
        "timeSeconds": time_seconds,
        "mistakes": mistakes,
        "hintsUsed": hints_used,
        "difficulty": difficulty,
        "dailyScore": daily_score,
        "submittedAt": SERVER_TIMESTAMP
    }, merge=True)

    return daily_score


def update_user_summary(user_id):
    today = datetime.utcnow()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    user_ref = db.collection("users").document(user_id)
    scores_ref = user_ref.collection("scores")

    monthly_scores = scores_ref.where("submittedAt", ">=", month_start).stream()

    total_score = 0
    total_time = 0
    count = 0

    for doc in monthly_scores:
        data = doc.to_dict()
        total_score += data.get("dailyScore", 0)
        total_time += data.get("timeSeconds", 0)
        count += 1

    avg_time = total_time / count if count > 0 else 0

    user_ref.set({
        "currentMonthTotal": total_score,
        "averageTime": avg_time,
        "updatedAt": SERVER_TIMESTAMP
    }, merge=True)

    return total_score, avg_time

def process_user_daily_submission(
    user_id: str,
    time_seconds: float,
    mistakes: int,
    hints_used: int,
    difficulty: int,
    date_str: str | None = None
):
    daily_score = submit_daily_score(
        user_id,
        time_seconds,
        mistakes,
        hints_used,
        difficulty,
        date_str=date_str
    )

    current_month_total, avg_time = update_user_summary(user_id)

    return {
        "dailyScore": daily_score,
        "currentMonthTotal": current_month_total,
        "averageTime": avg_time
    }

