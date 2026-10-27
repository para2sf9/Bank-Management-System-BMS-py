import tkinter as tk
from tkinter import ttk, messagebox

class PayrollView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Payroll", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.parent)
        top.pack(fill="x", pady=5)

        ttk.Label(top, text="Month").pack(side="left", padx=5)
        self.month = ttk.Combobox(top, values=[str(i) for i in range(1, 13)], state="readonly", width=5)
        self.month.set("1")
        self.month.pack(side="left", padx=5)

        ttk.Label(top, text="Year").pack(side="left", padx=5)
        self.year = ttk.Entry(top, width=8)
        self.year.insert(0, "2024")
        self.year.pack(side="left", padx=5)

        ttk.Button(top, text="Load", command=self.load_payroll).pack(side="left", padx=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(top, text="Generate Payroll", command=self.open_generate_window).pack(side="right", padx=5)

        cols = ("Employee ID", "Name", "Month", "Year", "Base Salary", "Bonus", "Deductions", "Net Salary")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)

        self.load_payroll()

    def load_payroll(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        month = int(self.month.get()) if self.month.get() else None
        year = int(self.year.get()) if self.year.get() else None
        records = self.db.get_payroll(month=month, year=year)
        emp_map = self.db.get_employee_names_map()
        for rec in records:
            self.tree.insert("", "end", values=(
                rec.get("employee_id", ""),
                emp_map.get(rec.get("employee_id", ""), ""),
                rec.get("month", ""),
                rec.get("year", ""),
                rec.get("base_salary", 0),
                rec.get("bonus", 0),
                rec.get("deductions", 0),
                rec.get("net_salary", 0)
            ))

    def open_generate_window(self):
        GeneratePayrollForm(self.parent, self.db, on_save=self.load_payroll)

class GeneratePayrollForm:
    def __init__(self, parent, db, on_save=None):
        self.db = db
        self.on_save = on_save
        self.win = tk.Toplevel(parent)
        self.win.title("Generate Payroll")
        self.win.geometry("500x500")
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

        ttk.Label(frame, text="Month").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.month = ttk.Combobox(frame, values=[str(i) for i in range(1, 13)], state="readonly", width=27)
        self.month.set("1")
        self.month.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Year").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.year = ttk.Entry(frame, width=30)
        self.year.insert(0, "2024")
        self.year.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Base Salary").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.base = ttk.Entry(frame, width=30)
        self.base.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Bonus").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.bonus = ttk.Entry(frame, width=30)
        self.bonus.insert(0, "0")
        self.bonus.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Deductions").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.deductions = ttk.Entry(frame, width=30)
        self.deductions.insert(0, "0")
        self.deductions.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(frame, text="Generate", command=self.save).grid(row=6, column=0, columnspan=2, pady=15)

    def save(self):
        emp = self.emp_combo.get().strip()
        if not emp:
            messagebox.showerror("Error", "Select an employee")
            return
        employee_id = emp.split(" - ")[0]
        try:
            base = float(self.base.get().strip())
            bonus = float(self.bonus.get().strip() or 0)
            deductions = float(self.deductions.get().strip() or 0)
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers for salary fields")
            return
        data = {
            "employee_id": employee_id,
            "month": int(self.month.get()),
            "year": int(self.year.get().strip()),
            "base_salary": base,
            "bonus": bonus,
            "deductions": deductions
        }
        success, msg = self.db.generate_payroll(data)
        if success:
            messagebox.showinfo("Success", msg)
            self.win.destroy()
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror("Error", msg)
