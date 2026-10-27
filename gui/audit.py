import tkinter as tk
from tkinter import ttk

class AuditView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Audit Logs", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.parent)
        top.pack(fill="x", pady=5)
        ttk.Button(top, text="Refresh", command=self.load_logs).pack(side="left", padx=5)

        cols = ("Timestamp", "Action", "Collection", "Document ID", "User", "Details")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=20)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=170, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)

        self.load_logs()

    def load_logs(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        logs = self.db.get_audit_logs(limit=500)
        for log in logs:
            ts = log.get("timestamp", "")
            ts_str = ts.strftime("%Y-%m-%d %H:%M:%S") if hasattr(ts, "strftime") else str(ts)
            self.tree.insert("", "end", values=(
                ts_str,
                log.get("action", ""),
                log.get("collection", ""),
                log.get("document_id", ""),
                log.get("user") or "",
                str(log.get("details") or "")
            ))
