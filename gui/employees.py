import tkinter as tk
from tkinter import ttk, messagebox
from gui.utils import ScrollableFrame

class EmployeesView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.selected_employee_id = None
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Employees", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.parent)
        top.pack(fill="x", pady=5)

        ttk.Label(top, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(top, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(top, text="Search", command=self.load_employees).pack(side="left", padx=5)
        ttk.Button(top, text="Refresh", command=self.load_employees).pack(side="left", padx=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(top, text="Add Employee", command=self.open_add_window).pack(side="right", padx=5)

        cols = ("Employee ID", "First Name", "Last Name", "Email", "Department", "Position", "Salary", "Status")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill="x", pady=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(btn_frame, text="Edit", command=self.open_edit_window).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Delete", command=self.delete_employee).pack(side="left", padx=5)

        self.load_employees()

    def load_employees(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        search = self.search_entry.get().strip() or None
        employees = self.db.get_employees(search=search)
        for emp in employees:
            self.tree.insert("", "end", iid=emp["employee_id"], values=(
                emp.get("employee_id", ""),
                emp.get("first_name", ""),
                emp.get("last_name", ""),
                emp.get("email", ""),
                emp.get("department_id", ""),
                emp.get("position", ""),
                emp.get("salary", 0),
                emp.get("status", "")
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_employee_id = selected[0]

    def open_add_window(self):
        EmployeeForm(self.parent, self.db, on_save=self.load_employees)

    def open_edit_window(self):
        if not self.selected_employee_id:
            messagebox.showwarning("Warning", "Select an employee first")
            return
        emp = self.db.get_employee_by_id(self.selected_employee_id)
        if not emp:
            messagebox.showerror("Error", "Employee not found")
            return
        EmployeeForm(self.parent, self.db, employee=emp, on_save=self.load_employees)

    def delete_employee(self):
        if not self.selected_employee_id:
            messagebox.showwarning("Warning", "Select an employee first")
            return
        if not messagebox.askyesno("Confirm", "Delete this employee?"):
            return
        success, msg = self.db.delete_employee(self.selected_employee_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.load_employees()
        else:
            messagebox.showerror("Error", msg)

class EmployeeForm:
    def __init__(self, parent, db, employee=None, on_save=None):
        self.db = db
        self.employee = employee
        self.on_save = on_save
        self.win = tk.Toplevel(parent)
        self.win.title("Edit Employee" if employee else "Add Employee")
        self.win.geometry("500x580")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.grab_set()
        self.build()

    def build(self):
        sf = ScrollableFrame(self.win)
        sf.pack(fill="both", expand=True, padx=10, pady=10)
        frame = sf.scrollable_frame

        ttk.Label(frame, text="Employee ID").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.emp_id = ttk.Entry(frame, width=30)
        self.emp_id.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="First Name").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.first_name = ttk.Entry(frame, width=30)
        self.first_name.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Last Name").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.last_name = ttk.Entry(frame, width=30)
        self.last_name.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Email").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.email = ttk.Entry(frame, width=30)
        self.email.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Phone").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.phone = ttk.Entry(frame, width=30)
        self.phone.grid(row=4, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Department ID").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.department = ttk.Entry(frame, width=30)
        self.department.grid(row=5, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Position").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.position = ttk.Entry(frame, width=30)
        self.position.grid(row=6, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Salary").grid(row=7, column=0, sticky="w", padx=5, pady=2)
        self.salary = ttk.Entry(frame, width=30)
        self.salary.grid(row=7, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Joining Date (YYYY-MM-DD)").grid(row=8, column=0, sticky="w", padx=5, pady=2)
        self.joining_date = ttk.Entry(frame, width=30)
        self.joining_date.grid(row=8, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Status").grid(row=9, column=0, sticky="w", padx=5, pady=2)
        self.status = ttk.Combobox(frame, values=["Active", "Inactive", "On Leave"], state="readonly", width=27)
        self.status.grid(row=9, column=1, sticky="w", padx=5, pady=2)
        self.status.set("Active")

        ttk.Button(frame, text="Save", command=self.save).grid(row=10, column=0, columnspan=2, pady=15)

        if self.employee:
            self.emp_id.insert(0, self.employee.get("employee_id", ""))
            self.emp_id.config(state="disabled")
            self.first_name.insert(0, self.employee.get("first_name", ""))
            self.last_name.insert(0, self.employee.get("last_name", ""))
            self.email.insert(0, self.employee.get("email", ""))
            self.phone.insert(0, self.employee.get("phone", ""))
            self.department.insert(0, self.employee.get("department_id", ""))
            self.position.insert(0, self.employee.get("position", ""))
            self.salary.insert(0, str(self.employee.get("salary", "")))
            self.joining_date.insert(0, self.employee.get("joining_date", ""))
            self.status.set(self.employee.get("status", "Active"))

    def save(self):
        data = {
            "employee_id": self.emp_id.get().strip(),
            "first_name": self.first_name.get().strip(),
            "last_name": self.last_name.get().strip(),
            "email": self.email.get().strip(),
            "phone": self.phone.get().strip(),
            "department_id": self.department.get().strip(),
            "position": self.position.get().strip(),
            "salary": self.salary.get().strip(),
            "joining_date": self.joining_date.get().strip(),
            "status": self.status.get()
        }
        if not data["employee_id"] or not data["first_name"] or not data["email"]:
            messagebox.showerror("Error", "Employee ID, First Name and Email are required")
            return
        if self.employee:
            success, msg = self.db.update_employee(data["employee_id"], data)
        else:
            success, msg = self.db.add_employee(data)
        if success:
            messagebox.showinfo("Success", msg)
            self.win.destroy()
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror("Error", msg)
