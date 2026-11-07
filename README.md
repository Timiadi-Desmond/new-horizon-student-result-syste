# New Horizon Student Result Management System

A local desktop application for managing secondary school student profiles, five-subject results, report cards and class performance. The program uses Python 3, Tkinter and a JSON file, so no database server or third-party package is required.

## Features

- Dashboard showing registrations, students with results, class average and top performer.
- Student registration, editing, deletion and search by ID or full name.
- Validated student IDs, required fields, gender and `YYYY-MM-DD` dates of birth.
- Entry and updating of Mathematics, English Language, Physics, Chemistry and Biology scores (0–100).
- Automatic totals, averages, grades and performance remarks.
- Individual report cards and sortable class performance reports, exported as text files.
- Automatic JSON save and load. Writes use a temporary file and replacement to reduce the chance of a partially written data file.

## Technologies

- Python 3.9 or later
- Tkinter (included with most Windows Python installations)
- Standard library: `json`, `os`, `datetime`, `re`, and `tkinter`

## Project structure

```text
student_result_system/
├── main.py             # Starts the application
├── gui.py              # Tkinter screens and user actions
├── student.py          # Student class and profile validation
├── results.py          # Subjects, score validation and calculations
├── storage.py          # JSON loading and saving
├── reports.py          # Individual and class text reports
├── dashboard.py        # Dashboard statistics
├── data/
│   └── students.json   # Created automatically when records are saved
└── README.md
```

## Run on Windows

1. Install Python 3 from [python.org](https://www.python.org/downloads/) and enable the option to add Python to PATH. Ensure the Tk/Tcl component is selected.
2. Open PowerShell in the project folder.
3. Start the app:

   ```powershell
   py main.py
   ```

The first run starts with an empty student list. Add a student, then use **Scores & Results** to enter scores. Records are stored in `data/students.json` beside the Python files. Back up that file when moving the project to another computer.

## Grading

The five subject scores are added for a total out of 500. The average is total divided by five. Grades are A (70–100), B (60–69), C (50–59), D (45–49), and F (below 45). Averages retain decimal precision for grading.

## JSON storage

Each student is stored as a JSON object containing identity fields, a subject-to-score dictionary and the result entry date. On startup the app loads the list. A missing file is treated as a new installation. Invalid JSON or invalid record shape is reported in a warning rather than crashing the window. Saving creates the data directory as needed and atomically replaces the previous file after writing a temporary copy.

## Python concepts demonstrated

- Variables, strings, numbers, dictionaries, lists and the subject tuple.
- Type conversion from score text to `float` and calculated numeric values.
- `if` / `elif` / `else` for validation, grades and remarks.
- `for` loops for subjects, records and report rows.
- Functions with parameters and return values across focused modules.
- Sorting with `sorted()` and key functions for names and averages.
- Exception handling around numeric conversion, dates, JSON and file operations.
- File handling with context managers and JSON serialization.
- Modules and imports separating interface, model, calculations, storage and reporting.
- Object-oriented programming through the `Student` class.
- `datetime` for date validation and result/report timestamps; `re` for ID validation.
- Input validation before records are saved.

## Notes

The app is intended for one administrator on one computer. It has no login system, network synchronization or multi-user conflict handling. Corrupted JSON is preserved for manual recovery; the app does not overwrite it automatically until a user saves a record.
