"""Dashboard statistics, kept separate from the interface."""
from results import average_for


def get_dashboard_stats(students):
    scored = [student for student in students if student.scores]
    averages = [(student, average_for(student.scores)) for student in scored]
    return {"total": len(students), "with_results": len(scored),
            "class_average": sum(value for _, value in averages) / len(averages) if averages else 0,
            "top_student": max(averages, key=lambda item: item[1]) if averages else None,
            # New registrations are appended, so the tail is the recent activity.
            "recent": list(reversed(students[-5:]))}
