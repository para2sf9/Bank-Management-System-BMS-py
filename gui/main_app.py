import tkinter as tk
from tkinter import ttk
from gui.dashboard import DashboardView
from gui.employees import EmployeesView
from gui.departments import DepartmentsView
from gui.attendance import AttendanceView
from gui.payroll import PayrollView
from gui.users import UsersView
from gui.branches import BranchesView
from gui.leaves import LeavesView
from gui.audit import AuditView

class MainApp:
    def __init__(self, root, user, db):
        self.root = root
        self.user = user
        self.db = db
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#f5f6fa")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Sidebar.TButton", font=("Helvetica", 11), padding=8)
        self.style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), background="#f5f6fa")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar = ttk.Frame(self.main_frame, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ttk.Frame(self.main_frame)
        self.content.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        self._build_sidebar()
        self.show_view("dashboard")

    def _build_sidebar(self):
        ttk.Label(self.sidebar, text="Bank Mgmt", font=("Helvetica", 16, "bold")).pack(pady=15)

        role = self.user.get("role", "")
        buttons = [("Dashboard", "dashboard")]

        if role in ("admin", "hr", "manager", "staff"):
            buttons.append(("Employees", "employees"))
            buttons.append(("Departments", "departments"))
            buttons.append(("Attendance", "attendance"))
            buttons.append(("Payroll", "payroll"))
            buttons.append(("Branches", "branches"))
            buttons.append(("Leaves", "leaves"))

        if role in ("admin", "hr"):
            buttons.append(("Audit Logs", "audit"))

        if role == "admin":
            buttons.append(("Users", "users"))

        for text, view in buttons:
            btn = ttk.Button(self.sidebar, text=text, command=lambda v=view: self.show_view(v), style="Sidebar.TButton")
            btn.pack(fill="x", padx=10, pady=3)

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=10)

        info = ttk.Label(self.sidebar, text=f"User: {self.user['username']}\nRole: {role}", justify="center")
        info.pack(pady=5)

        ttk.Button(self.sidebar, text="Logout", command=self.logout).pack(fill="x", padx=10, pady=10)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_view(self, view_name):
        self.clear_content()
        if view_name == "dashboard":
            DashboardView(self.content, self.db, self.user)
        elif view_name == "employees":
            EmployeesView(self.content, self.db, self.user)
        elif view_name == "departments":
            DepartmentsView(self.content, self.db, self.user)
        elif view_name == "attendance":
            AttendanceView(self.content, self.db, self.user)
        elif view_name == "payroll":
            PayrollView(self.content, self.db, self.user)
        elif view_name == "users":
            UsersView(self.content, self.db, self.user)
        elif view_name == "branches":
            BranchesView(self.content, self.db, self.user)
        elif view_name == "leaves":
            LeavesView(self.content, self.db, self.user)
        elif view_name == "audit":
            AuditView(self.content, self.db, self.user)

    def logout(self):
        self.root.destroy()
