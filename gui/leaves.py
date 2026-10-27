import tkinter as tk
from tkinter import ttk, messagebox
from gui.utils import ScrollableFrame

class LeavesView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.selected_leave_id = None
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Leaves", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.parent)
        top.pack(fill="x", pady=5)
        ttk.Button(top, text="Refresh", command=self.load_leaves).pack(side="left", padx=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(top, text="Add Leave", command=self.open_add_window).pack(side="right", padx=5)

        cols = ("Leave ID", "Employee ID", "Type", "Start Date", "End Date", "Status", "Reason")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill="x", pady=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(btn_frame, text="Edit Status", command=self.open_edit_window).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Delete", command=self.delete_leave).pack(side="left", padx=5)

        self.load_leaves()

    def load_leaves(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for leave in self.db.get_leaves():
            self.tree.insert("", "end", iid=str(leave["_id"]), values=(
                str(leave.get("_id", "")),
                leave.get("employee_id", ""),
                leave.get("leave_type", ""),
                leave.get("start_date", ""),
                leave.get("end_date", ""),
                leave.get("status", ""),
                leave.get("reason", "")
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_leave_id = selected[0]

    def open_add_window(self):
        LeaveForm(self.parent, self.db, on_save=self.load_leaves)

    def open_edit_window(self):
        if not self.selected_leave_id:
            messagebox.showwarning("Warning", "Select a leave record first")
            return
        leave = self.db.engine.find_one("leaves", {"_id": __import__("bson.objectid").objectid.ObjectId(self.selected_leave_id)})
        if not leave:
            messagebox.showerror("Error", "Leave not found")
            return
        LeaveForm(self.parent, self.db, leave=leave, on_save=self.load_leaves)

    def delete_leave(self):
        if not self.selected_leave_id:
            messagebox.showwarning("Warning", "Select a leave record first")
            return
        if not messagebox.askyesno("Confirm", "Delete this leave record?"):
            return
        success, msg = self.db.delete_leave(self.selected_leave_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.load_leaves()
        else:
            messagebox.showerror("Error", msg)

class LeaveForm:
    def __init__(self, parent, db, leave=None, on_save=None):
        self.db = db
        self.leave = leave
        self.on_save = on_save
        self.win = tk.Toplevel(parent)
        self.win.title("Edit Leave" if leave else "Add Leave")
        self.win.geometry("500x500")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.grab_set()
        self.build()

    def build(self):
        sf = ScrollableFrame(self.win)
        sf.pack(fill="both", expand=True, padx=10, pady=10)
        frame = sf.scrollable_frame

        ttk.Label(frame, text="Employee ID").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.emp_id = ttk.Entry(frame, width=30)
        self.emp_id.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Leave Type").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.leave_type = ttk.Combobox(frame, values=["Sick Leave", "Casual Leave", "Annual Leave", "Maternity Leave", "Other"], state="readonly", width=27)
        self.leave_type.set("Casual Leave")
        self.leave_type.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Start Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.start_date = ttk.Entry(frame, width=30)
        self.start_date.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="End Date (YYYY-MM-DD)").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.end_date = ttk.Entry(frame, width=30)
        self.end_date.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Status").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.status = ttk.Combobox(frame, values=["Pending", "Approved", "Rejected"], state="readonly", width=27)
        self.status.set("Pending")
        self.status.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Reason").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.reason = ttk.Entry(frame, width=30)
        self.reason.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(frame, text="Save", command=self.save).grid(row=6, column=0, columnspan=2, pady=15)

        if self.leave:
            self.emp_id.insert(0, self.leave.get("employee_id", ""))
            self.emp_id.config(state="disabled")
            self.leave_type.set(self.leave.get("leave_type", "Casual Leave"))
            self.start_date.insert(0, self.leave.get("start_date", ""))
            self.end_date.insert(0, self.leave.get("end_date", ""))
            self.status.set(self.leave.get("status", "Pending"))
            self.reason.insert(0, self.leave.get("reason", ""))

    def save(self):
        data = {
            "employee_id": self.emp_id.get().strip(),
            "leave_type": self.leave_type.get(),
            "start_date": self.start_date.get().strip(),
            "end_date": self.end_date.get().strip(),
            "status": self.status.get(),
            "reason": self.reason.get().strip()
        }
        if not data["employee_id"] or not data["start_date"] or not data["end_date"]:
            messagebox.showerror("Error", "Employee ID, Start Date and End Date are required")
            return
        if self.leave:
            from bson.objectid import ObjectId
            success, msg = self.db.update_leave(str(self.leave["_id"]), data)
        else:
            success, msg = self.db.add_leave(data)
        if success:
            messagebox.showinfo("Success", msg)
            self.win.destroy()
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror("Error", msg)
