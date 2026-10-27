import tkinter as tk
from tkinter import ttk, messagebox
from gui.utils import ScrollableFrame

class DepartmentsView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.selected_dept_id = None
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Departments", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.parent)
        top.pack(fill="x", pady=5)
        ttk.Button(top, text="Refresh", command=self.load_departments).pack(side="left", padx=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(top, text="Add Department", command=self.open_add_window).pack(side="right", padx=5)

        cols = ("Department ID", "Name", "Manager", "Location")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=220, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill="x", pady=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(btn_frame, text="Edit", command=self.open_edit_window).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Delete", command=self.delete_department).pack(side="left", padx=5)

        self.load_departments()

    def load_departments(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for dept in self.db.get_departments():
            self.tree.insert("", "end", iid=dept["department_id"], values=(
                dept.get("department_id", ""),
                dept.get("name", ""),
                dept.get("manager", ""),
                dept.get("location", "")
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_dept_id = selected[0]

    def open_add_window(self):
        DepartmentForm(self.parent, self.db, on_save=self.load_departments)

    def open_edit_window(self):
        if not self.selected_dept_id:
            messagebox.showwarning("Warning", "Select a department first")
            return
        dept = self.db.get_department_by_id(self.selected_dept_id)
        if not dept:
            messagebox.showerror("Error", "Department not found")
            return
        DepartmentForm(self.parent, self.db, department=dept, on_save=self.load_departments)

    def delete_department(self):
        if not self.selected_dept_id:
            messagebox.showwarning("Warning", "Select a department first")
            return
        if not messagebox.askyesno("Confirm", "Delete this department?"):
            return
        success, msg = self.db.delete_department(self.selected_dept_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.load_departments()
        else:
            messagebox.showerror("Error", msg)

class DepartmentForm:
    def __init__(self, parent, db, department=None, on_save=None):
        self.db = db
        self.department = department
        self.on_save = on_save
        self.win = tk.Toplevel(parent)
        self.win.title("Edit Department" if department else "Add Department")
        self.win.geometry("450x350")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.grab_set()
        self.build()

    def build(self):
        frame = ttk.Frame(self.win, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Department ID").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.dept_id = ttk.Entry(frame, width=30)
        self.dept_id.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Name").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name = ttk.Entry(frame, width=30)
        self.name.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Manager").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.manager = ttk.Entry(frame, width=30)
        self.manager.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Location").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.location = ttk.Entry(frame, width=30)
        self.location.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(frame, text="Save", command=self.save).grid(row=4, column=0, columnspan=2, pady=15)

        if self.department:
            self.dept_id.insert(0, self.department.get("department_id", ""))
            self.dept_id.config(state="disabled")
            self.name.insert(0, self.department.get("name", ""))
            self.manager.insert(0, self.department.get("manager", ""))
            self.location.insert(0, self.department.get("location", ""))

    def save(self):
        data = {
            "department_id": self.dept_id.get().strip(),
            "name": self.name.get().strip(),
            "manager": self.manager.get().strip(),
            "location": self.location.get().strip()
        }
        if not data["department_id"] or not data["name"]:
            messagebox.showerror("Error", "Department ID and Name are required")
            return
        if self.department:
            success, msg = self.db.update_department(data["department_id"], data)
        else:
            success, msg = self.db.add_department(data)
        if success:
            messagebox.showinfo("Success", msg)
            self.win.destroy()
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror("Error", msg)
