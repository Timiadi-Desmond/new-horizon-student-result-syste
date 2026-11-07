"""Application entry point."""
import tkinter as tk
from tkinter import messagebox
from gui import StudentResultApp
from storage import load_students


def main():
    students, warning = load_students()
    root = tk.Tk()
    if warning:
        messagebox.showwarning("Data file issue", warning + "\nThe app will start with an empty in-memory list.")
    StudentResultApp(root, students)
    root.mainloop()


if __name__ == "__main__":
    main()
