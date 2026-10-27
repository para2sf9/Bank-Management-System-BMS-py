import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from gui.utils import ScrollableFrame

class AttendanceView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Attendance", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.parent)
        top.pack(fill="x", pady=5)

        ttk.Label(top, text="Date (YYYY-MM-DD)").pack(side="left", padx=5)
        self.date_entry = ttk.Entry(top, width=12)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(side="left", padx=5)

        ttk.Button(top, text="Load", command=self.load_attendance).pack(side="left", padx=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(top, text="Mark Attendance", command=self.open_mark_window).pack(side="right", padx=5)

        cols = ("Employee ID", "Name", "Date", "Status", "Notes")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)

        self.load_attendance()

    def load_attendance(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        date = self.date_entry.get().strip()
        records = self.db.get_attendance(date=date)
        emp_map = self.db.get_employee_names_map()
        for rec in records:
            self.tree.insert("", "end", values=(
                rec.get("employee_id", ""),
                emp_map.get(rec.get("employee_id", ""), ""),
                rec.get("date", ""),
                rec.get("status", ""),
                rec.get("notes", "")
            ))

    def open_mark_window(self):
        MarkAttendanceForm(self.parent, self.db, on_save=self.load_attendance)

class MarkAttendanceForm:
    def __init__(self, parent, db, on_save=None):
        self.db = db
        self.on_save = on_save
        self.win = tk.Toplevel(parent)
        self.win.title("Mark Attendance")
        self.win.geometry("500x450")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.grab_set()
        self.build()

    def build(self):
        frame = ttk.Frame(self.win, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Employee").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        employees = self.db.get_employees()
        self.emp_combo = ttk.Combobox(frame, values=[f"{e['employee_id']} - {e['first_name']} {e['last_name']}" for e in employees], state="readonly", width=30)
        self.emp_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Date (YYYY-MM-DD)").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.date = ttk.Entry(frame, width=30)
        self.date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Status").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.status = ttk.Combobox(frame, values=["Present", "Absent", "On Leave", "Half Day"], state="readonly", width=27)
        self.status.set("Present")
        self.status.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Notes").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.notes = ttk.Entry(frame, width=30)
        self.notes.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(frame, text="Save", command=self.save).grid(row=4, column=0, columnspan=2, pady=15)

    def save(self):
        emp = self.emp_combo.get().strip()
        if not emp:
            messagebox.showerror("Error", "Select an employee")
            return
        employee_id = emp.split(" - ")[0]
        data = {
            "employee_id": employee_id,
            "date": self.date.get().strip(),
            "status": self.status.get(),
            "notes": self.notes.get().strip()
        }
        success, msg = self.db.mark_attendance(data)
        if success:
            messagebox.showinfo("Success", msg)
            self.win.destroy()
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror("Error", msg)
