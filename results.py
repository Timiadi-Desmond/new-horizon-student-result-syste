"""Score entry and academic calculations."""
from datetime import datetime

SUBJECTS = ("Mathematics", "English Language", "Physics", "Chemistry", "Biology")


def validate_scores(scores):
    if not all(subject in scores for subject in SUBJECTS):
        return "Enter a score for all five subjects."
    try:
        values = [float(scores[subject]) for subject in SUBJECTS]
    except (TypeError, ValueError):
        return "Scores must be numbers."
    if any(value < 0 or value > 100 for value in values):
        return "Each score must be between 0 and 100."
    return ""


def grade_for(average):
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 45:
        return "D"
    return "F"


def total_for(scores):
    return sum(float(scores[subject]) for subject in SUBJECTS)


def average_for(scores):
    return total_for(scores) / len(SUBJECTS)


def performance_remark(average):
    if average >= 70:
        return "Excellent performance. Keep it up!"
    elif average >= 60:
        return "Very good performance."
    elif average >= 50:
        return "Good effort. Keep working hard."
    elif average >= 45:
        return "Fair performance. More practice is recommended."
    return "Needs improvement. Please seek additional support."


def record_scores(student, scores):
    error = validate_scores(scores)
    if error:
        raise ValueError(error)
    student.scores = {subject: float(scores[subject]) for subject in SUBJECTS}
    student.result_date = datetime.now().strftime("%Y-%m-%d %H:%M")
