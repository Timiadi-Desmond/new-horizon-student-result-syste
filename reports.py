"""Text report card and class report generation."""
from datetime import datetime
from results import SUBJECTS, average_for, grade_for, performance_remark, total_for


def report_card(student):
    if not student.scores:
        raise ValueError("This student has no recorded results yet.")
    average = average_for(student.scores)
    lines = ["NEW HORIZON", "STUDENT REPORT CARD", "=" * 42,
             f"Student: {student.full_name}", f"Student ID: {student.student_id}",
             f"Class/Form: {student.class_form}", f"Date of birth: {student.date_of_birth}",
             "", "SUBJECT SCORES", "-" * 42]
    lines.extend(f"{subject:<24} {student.scores[subject]:>6g}" for subject in SUBJECTS)
    lines.extend(["-" * 42, f"Total: {total_for(student.scores):.1f} / 500",
                  f"Average: {average:.1f}%", f"Overall grade: {grade_for(average)}",
                  f"Result entered: {student.result_date or 'Unknown'}",
                  f"Remark: {performance_remark(average)}"])
    return "\n".join(lines)


def class_report(students, sort_by="average"):
    with_results = [student for student in students if student.scores]
    if sort_by == "name":
        ordered = sorted(students, key=lambda student: student.full_name.lower())
    else:
        ordered = sorted(students, key=lambda student: average_for(student.scores)
                         if student.scores else -1, reverse=True)
    averages = [average_for(student.scores) for student in with_results]
    lines = ["NEW HORIZON — CLASS PERFORMANCE REPORT",
             f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
             f"Registered students: {len(students)}",
             f"Students with results: {len(with_results)}"]
    if averages:
        lines.extend([f"Class average: {sum(averages) / len(averages):.1f}%",
                      f"Highest average: {max(averages):.1f}%",
                      f"Lowest average: {min(averages):.1f}%"])
    else:
        lines.append("Class average: No results recorded")
    lines.extend(["", f"{'ID':<14}{'Student':<27}{'Class':<14}{'Average':>9}{'Grade':>8}", "-" * 72])
    for student in ordered:
        average = average_for(student.scores) if student.scores else None
        lines.append(f"{student.student_id:<14}{student.full_name:<27}{student.class_form:<14}"
                     f"{(f'{average:.1f}%' if average is not None else 'No result'):>9}"
                     f"{(grade_for(average) if average is not None else '—'):>8}")
    return "\n".join(lines)
