"""Tkinter user interface for the Student Result Management System."""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from student import Student, validate_student
from results import SUBJECTS, average_for, grade_for, record_scores
from reports import report_card, class_report
from dashboard import get_dashboard_stats
from storage import save_students

NAVY = "#14263D"
TEAL = "#138A83"
BG = "#F3F6FA"
INK = "#243449"


class StudentResultApp:
    def __init__(self, root, students):
        self.root, self.students = root, students
        self.selected_id = None
        root.title("New Horizon | Student Result Management")
        root.geometry("1180x760")
        root.minsize(900, 620)
        root.configure(bg=BG)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", rowheight=34, font=("Segoe UI", 10),
                             background="white", fieldbackground="white", foreground=INK)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                             background="#E8EEF5", foreground=NAVY)
        shell = tk.Frame(root, bg=BG)
        shell.pack(fill="both", expand=True)
        sidebar = tk.Frame(shell, bg=NAVY, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="NEW HORIZON", bg=NAVY, fg="white",
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=22, pady=(28, 2))
        tk.Label(sidebar, text="STUDENT SERVICES", bg=NAVY, fg="#A9BBCD",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=23, pady=(0, 28))
        self.content = tk.Frame(shell, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)
        for label, callback in (("▦  Dashboard", self.show_dashboard),
                                ("♙  Students", self.show_students),
                                ("▤  Scores & Results", self.show_scores),
                                ("▧  Class Reports", self.show_reports)):
            tk.Button(sidebar, text=label, command=callback, anchor="w", relief="flat",
                      bg=NAVY, fg="white", activebackground="#263D58", activeforeground="white",
                      font=("Segoe UI", 11), padx=22, pady=13, cursor="hand2").pack(fill="x")
        self.show_dashboard()

    def persist(self):
        try:
            save_students(self.students)
        except OSError as error:
            messagebox.showerror("Save error", f"Records could not be saved:\n{error}")

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle=""):
        self.clear()
        head = tk.Frame(self.content, bg=BG)
        head.pack(fill="x", padx=30, pady=(26, 18))
        tk.Label(head, text=title, bg=BG, fg=NAVY,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(head, text=subtitle, bg=BG, fg="#6B7C91",
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 0))
        return head

    def button(self, parent, text, command, color=TEAL):
        return tk.Button(parent, text=text, command=command, bg=color, fg="white",
                         activebackground=color, activeforeground="white", relief="flat",
                         padx=15, pady=9, font=("Segoe UI", 10, "bold"), cursor="hand2")

    def show_dashboard(self):
        self.heading("Dashboard", "A quick overview of student registration and class performance")
        stats = get_dashboard_stats(self.students)
        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", padx=24)
        card_data = [("REGISTERED STUDENTS", str(stats["total"]), NAVY),
                     ("WITH RESULTS", str(stats["with_results"]), TEAL),
                     ("CLASS AVERAGE", f"{stats['class_average']:.1f}%" if stats["with_results"] else "—", "#4B6B91"),
                     ("TOP PERFORMER", stats["top_student"][0].full_name if stats["top_student"] else "—", "#21836F")]
        for title, value, color in card_data:
            card = tk.Frame(cards, bg="white", highlightbackground="#E4EAF0", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=6, pady=4)
            tk.Label(card, text=title, bg="white", fg="#708096", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=16, pady=(15, 5))
            tk.Label(card, text=value, bg="white", fg=color, font=("Segoe UI", 18, "bold"), wraplength=190).pack(anchor="w", padx=16, pady=(0, 16))
        tk.Label(self.content, text="Recent registrations", bg=BG, fg=NAVY,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=30, pady=(26, 10))
        recent = list(reversed(self.students[-8:]))
        self.make_tree(self.content, ("id", "name", "class", "gender"),
                       ("Student ID", "Full name", "Class/Form", "Gender"), height=10)
        for s in recent:
            self.tree.insert("", "end", values=(s.student_id, s.full_name, s.class_form, s.gender))

    def make_tree(self, parent, keys, labels, height=14):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.tree = ttk.Treeview(frame, columns=keys, show="headings", height=height)
        for key, label in zip(keys, labels):
            self.tree.heading(key, text=label)
            self.tree.column(key, width=150, anchor="w")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return self.tree

    def show_students(self):
        self.heading("Students", "Register, find and maintain student profiles")
        bar = tk.Frame(self.content, bg=BG); bar.pack(fill="x", padx=30, pady=(0, 12))
        self.search_var = tk.StringVar()
        entry = ttk.Entry(bar, textvariable=self.search_var, width=32)
        entry.pack(side="left", ipady=6)
        entry.bind("<KeyRelease>", lambda _event: self.populate_students())
        self.button(bar, "＋ Add student", self.student_form).pack(side="right", padx=4)
        self.button(bar, "Edit selected", self.edit_selected, color="#496887").pack(side="right", padx=4)
        self.button(bar, "Delete", self.delete_selected, color="#C45159").pack(side="right", padx=4)
        self.make_tree(self.content, ("id", "name", "class", "gender", "dob"),
                       ("Student ID", "Full name", "Class/Form", "Gender", "Date of birth"))
        self.populate_students()

    def populate_students(self):
        if not hasattr(self, "tree") or not self.tree.winfo_exists(): return
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().strip().lower()
        for s in sorted(self.students, key=lambda item: item.full_name.lower()):
            if query in s.student_id.lower() or query in s.full_name.lower():
                self.tree.insert("", "end", values=(s.student_id, s.full_name, s.class_form, s.gender, s.date_of_birth))

    def selected_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select a student", "Select a student row first."); return None
        student_id = self.tree.item(selected[0], "values")[0]
        return next((s for s in self.students if s.student_id == student_id), None)

    def student_form(self, existing=None):
        win = tk.Toplevel(self.root); win.title("Edit student" if existing else "Add student")
        win.transient(self.root); win.grab_set(); win.configure(bg=BG); win.resizable(False, False)
        tk.Label(win, text="Student information", bg=BG, fg=NAVY, font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=22, pady=18, sticky="w")
        labels = ["Student ID", "Full name", "Class/Form", "Gender", "Date of birth (YYYY-MM-DD)"]
        values = [existing.student_id, existing.full_name, existing.class_form, existing.gender, existing.date_of_birth] if existing else ["", "", "", "", ""]
        vars_ = []
        for row, (label, value) in enumerate(zip(labels, values), start=1):
            tk.Label(win, text=label, bg=BG, fg=INK, font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", padx=22, pady=6)
            var = tk.StringVar(value=value); vars_.append(var)
            if label == "Gender":
                field = ttk.Combobox(win, textvariable=var, values=("Female", "Male", "Other"), state="readonly", width=27)
            else:
                field = ttk.Entry(win, textvariable=var, width=30)
            field.grid(row=row, column=1, padx=(10, 22), pady=6, ipady=4)
        def submit():
            vals = [var.get() for var in vars_]
            error = validate_student(*vals)
            if error: messagebox.showerror("Check student details", error, parent=win); return
            sid = vals[0].strip().upper()
            if any(s.student_id == sid and s is not existing for s in self.students):
                messagebox.showerror("Duplicate ID", "That student ID is already registered.", parent=win); return
            if existing:
                existing.student_id, existing.full_name, existing.class_form, existing.gender, existing.date_of_birth = sid, vals[1].strip(), vals[2].strip(), vals[3], vals[4]
            else:
                self.students.append(Student(*vals))
            self.persist(); win.destroy()
            if existing: self.show_students()
            else: self.show_students()
        self.button(win, "Save student", submit).grid(row=6, column=0, columnspan=2, pady=18)

    def edit_selected(self):
        student = self.selected_student()
        if student: self.student_form(student)

    def delete_selected(self):
        student = self.selected_student()
        if student and messagebox.askyesno("Delete student", f"Permanently delete {student.full_name} and their results?"):
            self.students.remove(student); self.persist(); self.populate_students()

    def show_scores(self):
        self.heading("Scores & Results", "Record all five subject scores and review calculated results")
        bar = tk.Frame(self.content, bg=BG); bar.pack(fill="x", padx=30, pady=(0, 12))
        self.button(bar, "Record / update scores", self.score_form).pack(side="left")
        self.button(bar, "View report card", self.show_card, color="#496887").pack(side="left", padx=8)
        self.make_tree(self.content, ("id", "name", "class", "total", "average", "grade"),
                       ("Student ID", "Full name", "Class", "Total / 500", "Average", "Grade"))
        for s in sorted(self.students, key=lambda item: item.full_name.lower()):
            if s.scores:
                avg = average_for(s.scores)
                self.tree.insert("", "end", values=(s.student_id, s.full_name, s.class_form, f"{sum(s.scores.values()):.1f}", f"{avg:.1f}%", grade_for(avg)))

    def score_form(self):
        if not self.students:
            messagebox.showinfo("No students", "Register a student before entering results."); return
        win = tk.Toplevel(self.root); win.title("Record scores"); win.transient(self.root); win.grab_set(); win.configure(bg=BG)
        tk.Label(win, text="Select student", bg=BG, fg=INK).grid(row=0, column=0, padx=20, pady=12, sticky="w")
        choices = [f"{s.student_id} — {s.full_name}" for s in self.students]
        selected = tk.StringVar(value=choices[0]); ttk.Combobox(win, textvariable=selected, values=choices, state="readonly", width=38).grid(row=0, column=1, padx=20, pady=12)
        fields = {}
        for row, subject in enumerate(SUBJECTS, start=1):
            tk.Label(win, text=subject, bg=BG, fg=INK).grid(row=row, column=0, padx=20, pady=7, sticky="w")
            value = tk.StringVar(); fields[subject] = value
            ttk.Entry(win, textvariable=value, width=18).grid(row=row, column=1, padx=20, pady=7, sticky="w")
        def choose(event=None):
            sid = selected.get().split(" — ", 1)[0]
            student = next(s for s in self.students if s.student_id == sid)
            for subject in SUBJECTS: fields[subject].set(str(student.scores.get(subject, "")))
        choose(); win.bind("<<ComboboxSelected>>", choose)
        def submit():
            sid = selected.get().split(" — ", 1)[0]
            student = next(s for s in self.students if s.student_id == sid)
            try:
                scores = {subject: float(fields[subject].get().strip()) for subject in SUBJECTS}
                record_scores(student, scores)
            except ValueError as error:
                messagebox.showerror("Invalid scores", str(error), parent=win); return
            self.persist(); win.destroy(); self.show_scores()
        self.button(win, "Save results", submit).grid(row=6, column=0, columnspan=2, pady=15)

    def show_card(self):
        student = self.selected_student()
        if not student: return
        try: text = report_card(student)
        except ValueError as error: messagebox.showinfo("No results", str(error)); return
        if not messagebox.askyesno("Report card", text + "\n\nSave this report card as a text file?"): return
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"{student.student_id}_report_card.txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as file: file.write(text)
            messagebox.showinfo("Exported", f"Report card saved to:\n{path}")

    def show_reports(self):
        self.heading("Class Reports", "Class statistics, student ranking and export")
        bar = tk.Frame(self.content, bg=BG); bar.pack(fill="x", padx=30, pady=(0, 12))
        self.sort_var = tk.StringVar(value="Highest average")
        choice = ttk.Combobox(bar, textvariable=self.sort_var, values=("Highest average", "Alphabetical name"), state="readonly", width=22)
        choice.pack(side="left"); choice.bind("<<ComboboxSelected>>", lambda _e: self.populate_reports())
        self.button(bar, "Save class report", self.export_class).pack(side="right")
        self.make_tree(self.content, ("id", "name", "class", "average", "grade"),
                       ("Student ID", "Full name", "Class/Form", "Average", "Grade"))
        self.populate_reports()

    def populate_reports(self):
        self.tree.delete(*self.tree.get_children())
        by_name = getattr(self, "sort_var", tk.StringVar(value="Highest average")).get() == "Alphabetical name"
        ordered = sorted(self.students, key=(lambda s: s.full_name.lower()) if by_name else (lambda s: average_for(s.scores) if s.scores else -1), reverse=not by_name)
        for s in ordered:
            avg = average_for(s.scores) if s.scores else None
            self.tree.insert("", "end", values=(s.student_id, s.full_name, s.class_form,
                              f"{avg:.1f}%" if avg is not None else "No result",
                              grade_for(avg) if avg is not None else "—"))

    def export_class(self):
        sort_by = "name" if self.sort_var.get() == "Alphabetical name" else "average"
        text = class_report(self.students, sort_by)
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="new_horizon_class_report.txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as file: file.write(text)
            messagebox.showinfo("Exported", f"Class report saved to:\n{path}")
