"""Student model and input validation for New Horizon Result Management."""
from datetime import datetime


class Student:
    """A student's identity and optional subject scores."""

    def __init__(self, student_id, full_name, class_form, gender, date_of_birth,
                 scores=None, result_date=""):
        self.student_id = student_id.strip().upper()
        self.full_name = full_name.strip()
        self.class_form = class_form.strip()
        self.gender = gender.strip()
        self.date_of_birth = date_of_birth.strip()
        self.scores = dict(scores or {})
        self.result_date = result_date

    def to_dict(self):
        return {"student_id": self.student_id, "full_name": self.full_name,
                "class_form": self.class_form, "gender": self.gender,
                "date_of_birth": self.date_of_birth, "scores": self.scores,
                "result_date": self.result_date}

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["full_name"], data["class_form"],
                   data["gender"], data["date_of_birth"], data.get("scores", {}),
                   data.get("result_date", ""))


def validate_student(student_id, full_name, class_form, gender, date_of_birth):
    """Return an error message, or an empty string when the fields are valid."""
    if not all(value.strip() for value in
               (student_id, full_name, class_form, gender, date_of_birth)):
        return "Please complete every student field."
    # Schools commonly use formats such as NH/2025/001, so allow separators
    # beyond hyphens and underscores while rejecting control characters.
    clean_id = student_id.strip()
    if len(clean_id) > 40 or any(ord(character) < 32 for character in clean_id):
        return "Student ID must be 40 characters or fewer and contain no control characters."
    if len(full_name.strip()) < 2:
        return "Enter a full name with at least two characters."
    if gender not in ("Female", "Male", "Other"):
        return "Select a valid gender."
    try:
        birth_date = datetime.strptime(date_of_birth.strip(), "%Y-%m-%d").date()
    except ValueError:
        return "Date of birth must use YYYY-MM-DD (for example, 2010-05-21)."
    if birth_date > datetime.today().date():
        return "Date of birth cannot be in the future."
    return ""
