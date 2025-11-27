import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os

FILE_NAME = "studentMarks.txt"

# CODE FOR FILE HANDLING

def load_students():
    students = []

    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", "studentMarks.txt file not found")
        return students

    with open(FILE_NAME, "r") as file:
        lines = file.readlines()

    for line in lines[1:]:
        parts = line.strip().split(",")

        student = {
            "code": parts[0],
            "name": parts[1],
            "c1": int(parts[2]),
            "c2": int(parts[3]),
            "c3": int(parts[4]),
            "exam": int(parts[5])
        }

        students.append(student)

    return students


def save_students(students):
    with open(FILE_NAME, "w") as file:
        file.write(str(len(students)) + "\n")
        for s in students:
            line = f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n"
            file.write(line)

# CODE FOR MARK CALCULATIONS

def total_mark(s):
    return s["c1"] + s["c2"] + s["c3"] + s["exam"]

def percentage(s):
    return (total_mark(s) / 160) * 100

def grade(p):
    if p >= 70: return "A"
    elif p >= 60: return "B"
    elif p >= 50: return "C"
    elif p >= 40: return "D"
    else: return "F"

# CODE FOR TABLE DISPLAY FUNCTIONS

def clear_table():
    global row_count
    row_count = 0
    for row in student_table.get_children():
        student_table.delete(row)


row_count = 0

def insert_student(s):
    global row_count

    tag = "evenrow" if row_count % 2 == 0 else "oddrow"

    student_table.insert("", tk.END, values=(
        s["code"],
        s["name"],
        s["c1"],
        s["c2"],
        s["c3"],
        s["exam"],
        total_mark(s),
        f"{percentage(s):.2f}%",
        grade(percentage(s))
    ), tags=(tag,))

    row_count += 1

#CODE FOR BUTTON FUNCTIONS

def view_all():
    students = load_students()
    clear_table()
    for s in students:
        insert_student(s)

def view_individual():
    students = load_students()
    key = simpledialog.askstring("Search", "Enter Name or Code:")

    clear_table()
    for s in students:
        if s["code"] == key or s["name"].lower() == key.lower():
            insert_student(s)
            return

    messagebox.showerror("Not Found", "Student not found")

def show_highest():
    students = load_students()
    best = max(students, key=percentage)
    clear_table()
    insert_student(best)

def show_lowest():
    students = load_students()
    worst = min(students, key=percentage)
    clear_table()
    insert_student(worst)

def sort_students():
    students = load_students()
    order = simpledialog.askstring("Sort", "Type ASC or DESC:")
    students.sort(key=percentage, reverse=(order and order.upper() == "DESC"))

    clear_table()
    for s in students:
        insert_student(s)

def add_student():
    students = load_students()

    code = simpledialog.askstring("Add", "Enter Code:")
    name = simpledialog.askstring("Add", "Enter Name:")
    c1 = int(simpledialog.askstring("Add", "Coursework 1:"))
    c2 = int(simpledialog.askstring("Add", "Coursework 2:"))
    c3 = int(simpledialog.askstring("Add", "Coursework 3:"))
    exam = int(simpledialog.askstring("Add", "Exam:"))

    students.append({"code": code, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam})
    save_students(students)

    messagebox.showinfo("Success", "Student Added Successfully")
    view_all()

def delete_student():
    students = load_students()
    key = simpledialog.askstring("Delete", "Enter Name or Code:")

    students = [s for s in students if s["code"] != key and s["name"].lower() != key.lower()]
    save_students(students)

    messagebox.showinfo("Deleted", "Student Removed")
    view_all()

def update_student():
    students = load_students()
    key = simpledialog.askstring("Update", "Enter Name or Code:")

    for s in students:
        if s["code"] == key or s["name"].lower() == key.lower():
            s["c1"] = int(simpledialog.askstring("Update", "New Coursework 1:"))
            s["c2"] = int(simpledialog.askstring("Update", "New Coursework 2:"))
            s["c3"] = int(simpledialog.askstring("Update", "New Coursework 3:"))
            s["exam"] = int(simpledialog.askstring("Update", "New Exam Mark:"))
            save_students(students)

            messagebox.showinfo("Updated", "Student Record Updated")
            view_all()
            return

# MAIN WINDOW CODE

root = tk.Tk()
root.title("Student Management System")
root.geometry("1300x750")
root.configure(bg="#0f172a")

#CHANGE ICON CODE
try:
    icon_image = tk.PhotoImage(file="Studentmanagment.png")
    root.iconphoto(False, icon_image)
except Exception as e:
    print("Icon file not found or invalid:", e)

# HOME PAGE CODE

home_frame = tk.Frame(root, bg="#020617")
home_frame.pack(fill="both", expand=True)

home_title = tk.Label(home_frame, text="STUDENT MANAGEMENT SYSTEM",
                      font=("Segoe UI", 28, "bold"), fg="white", bg="#020617")
home_title.pack(pady=80)

def enter_system():
    home_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

enter_btn = tk.Button(home_frame, text="ENTER SYSTEM",
                      font=("Segoe UI", 14, "bold"), bg="#2563eb",
                      fg="white", padx=40, pady=14,
                      bd=0, command=enter_system)
enter_btn.pack(pady=50)

# CODE FOR MAIN SYSTEM FRAME

main_frame = tk.Frame(root, bg="#020617")

sidebar = tk.Frame(main_frame, bg="#020617", width=260)
sidebar.pack(side="left", fill="y")

display = tk.Frame(main_frame, bg="white")
display.pack(side="right", fill="both", expand=True, padx=10, pady=10)

#CODE FOR BUTTONS

def styled_button(text, cmd):
    btn = tk.Button(sidebar, text=text, command=cmd,
                    font=("Segoe UI", 11, "bold"),
                    bg="#1e40af", fg="white",
                    bd=0, pady=14)
    btn.pack(fill="x", padx=12, pady=6)
    btn.bind("<Enter>", lambda e: btn.config(bg="#2563eb"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#1e40af"))

styled_button("View All Students", view_all)
styled_button("View Individual Student", view_individual)
styled_button("Highest Score", show_highest)
styled_button("Lowest Score", show_lowest)
styled_button("Sort Records", sort_students)
styled_button("Add Student", add_student)
styled_button("Delete Student", delete_student)
styled_button("Update Student", update_student)

exit_btn = tk.Button(sidebar, text="Exit System",
                     bg="#dc2626", fg="white",
                     font=("Segoe UI", 11, "bold"),
                     bd=0, pady=16, command=root.destroy)
exit_btn.pack(fill="x", padx=10, pady=30)

#CODE FOR TABLE DISPLAY
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                 background="white",
                 foreground="black",
                 rowheight=32,
                 fieldbackground="white",
                 bordercolor="#d1d5db",
                 borderwidth=1,
                 font=("Segoe UI", 10))

style.configure("Treeview.Heading",
                 background="#1e3a8a",
                 foreground="white",
                 font=("Segoe UI", 11, "bold"),
                 relief="flat")

style.map("Treeview.Heading",
          background=[("active", "#2563eb")])

columns = ("Code", "Name", "C1", "C2", "C3", "Exam", "Total", "Percent", "Grade")

student_table = ttk.Treeview(display, columns=columns, show="headings", style="Treeview")

student_table.heading("Code", text="Student Code")
student_table.heading("Name", text="Student Name")
student_table.heading("C1", text="Course 1")
student_table.heading("C2", text="Course 2")
student_table.heading("C3", text="Course 3")
student_table.heading("Exam", text="Exam")
student_table.heading("Total", text="Total")
student_table.heading("Percent", text="Percentage")
student_table.heading("Grade", text="Grade")

student_table.column("Code", width=110, anchor="center")
student_table.column("Name", width=200, anchor="w")
student_table.column("C1", width=80, anchor="center")
student_table.column("C2", width=80, anchor="center")
student_table.column("C3", width=80, anchor="center")
student_table.column("Exam", width=90, anchor="center")
student_table.column("Total", width=90, anchor="center")
student_table.column("Percent", width=100, anchor="center")
student_table.column("Grade", width=80, anchor="center")

student_table.pack(fill="both", expand=True, padx=10, pady=10)

#CODE FOR ROW COLORS

style.configure("oddrow", background="white")
style.configure("evenrow", background="#f1f5f9")


root.mainloop()
