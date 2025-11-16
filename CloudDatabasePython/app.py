from flask import Flask, request, jsonify, send_from_directory
import os
from services.firestore_client import get_db
from services.user_summary import process_user_daily_submission
from services.leaderboard import get_current_month_leaderboard  # 👈 NEW

app = Flask(__name__)
db = get_db()

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route("/users", methods=["GET"])
def list_users():
    users_ref = db.collection("users")
    docs = users_ref.stream()
    users = [{"userId": doc.id, "username": doc.to_dict().get("username", doc.id)} for doc in docs]
    return jsonify(users)

@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.json
    result = process_user_daily_submission(
        data["userId"],
        data["timeSeconds"],
        data["mistakes"],
        data["hintsUsed"],
        data["difficulty"],
        date_str=data.get("date")
    )
    result["submittedBy"] = data.get("submittedBy", "anonymous")
    return jsonify(result)


# leaderboard data endpoint
@app.route("/leaderboard-data", methods=["GET"])
def leaderboard_data():
    leaderboard = get_current_month_leaderboard()
    return jsonify(leaderboard)

if __name__ == "__main__":
    app.run(debug=True)
