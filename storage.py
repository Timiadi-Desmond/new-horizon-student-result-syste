"""JSON persistence for student records."""
import json
import os
from student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Load students; a missing or malformed file is handled without crashing."""
    if not os.path.exists(path):
        return [], ""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("The top-level JSON value must be a list.")
        students = [Student.from_dict(item) for item in data]
        return students, ""
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
        return [], f"Could not load {path}: {error}"
    finally:
        pass


def save_students(students, path=DATA_FILE):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    temporary_path = path + ".tmp"
    try:
        with open(temporary_path, "w", encoding="utf-8") as file:
            json.dump([student.to_dict() for student in students], file,
                      indent=2, ensure_ascii=False)
        os.replace(temporary_path, path)
    except OSError:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)
        raise
