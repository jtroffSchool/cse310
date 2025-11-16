def calculate_daily_score(time_seconds, mistakes, hints_used, difficulty):
    score = (
        1000
        - (time_seconds * 0.5)
        - (50 * mistakes)
        - (25 * hints_used)
        + (10 * difficulty)
    )
    return max(int(score), 0)
