import tkinter as tk
from tkinter import ttk

class DashboardView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Dashboard", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        stats = self.db.get_stats()

        cards_frame = ttk.Frame(self.parent)
        cards_frame.pack(fill="x", pady=10)

        items = [
            ("Total Employees", stats.get("total_employees", 0)),
            ("Total Departments", stats.get("total_departments", 0)),
            ("Present Today", stats.get("present_today", 0)),
            ("Total Branches", stats.get("total_branches", 0)),
        ]

        for i, (label, value) in enumerate(items):
            card = ttk.Frame(cards_frame, relief="solid", padding=15)
            card.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            ttk.Label(card, text=str(value), font=("Helvetica", 22, "bold")).pack()
            ttk.Label(card, text=label, font=("Helvetica", 11)).pack()

        for i in range(len(items)):
            cards_frame.columnconfigure(i, weight=1)

        ttk.Label(self.parent, text="Quick Info", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(20, 5))
        info_text = (
            "Modules available based on your role:\n"
            "- Employees, Departments, Attendance, Payroll, Branches, Leaves\n"
            "- Admin: Users and Audit Logs\n\n"
            "Database features enabled:\n"
            "Connection Pooling, ACID Transactions, Indexing, Soft Deletes, Aggregation, Audit Logging"
        )
        info = ttk.Label(self.parent, text=info_text, justify="left")
        info.pack(anchor="w")
