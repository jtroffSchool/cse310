from services.user_summary import process_user_daily_submission

def main():
    user_id = "test_user_123"

    # Example user submission
    submission_data = {
        "time_seconds": 23.7,
        "mistakes": 1,
        "hints_used": 0,
        "difficulty": 4
    }

    result = process_user_daily_submission(
        user_id,
        submission_data["time_seconds"],
        submission_data["mistakes"],
        submission_data["hints_used"],
        submission_data["difficulty"]
    )

    print("Submission Result:")
    print(f"Daily Score: {result['dailyScore']}")
    print(f"Current Month Total: {result['currentMonthTotal']}")
    print(f"Average Time: {result['averageTime']:.2f} seconds")


if __name__ == "__main__":
    main()
