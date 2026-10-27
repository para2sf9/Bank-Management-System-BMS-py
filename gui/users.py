import tkinter as tk
from tkinter import ttk, messagebox

class UsersView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.selected_username = None
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Users", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.parent)
        top.pack(fill="x", pady=5)
        ttk.Button(top, text="Refresh", command=self.load_users).pack(side="left", padx=5)
        ttk.Button(top, text="Add User", command=self.open_add_window).pack(side="right", padx=5)

        cols = ("Username", "Role", "Employee ID")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=300, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_user).pack(side="left", padx=5)

        self.load_users()

    def load_users(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for u in self.db.get_users():
            self.tree.insert("", "end", iid=u["username"], values=(
                u.get("username", ""),
                u.get("role", ""),
                u.get("employee_id", "") or ""
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_username = selected[0]

    def open_add_window(self):
        UserForm(self.parent, self.db, on_save=self.load_users)

    def delete_user(self):
        if not self.selected_username:
            messagebox.showwarning("Warning", "Select a user first")
            return
        if self.selected_username == "admin":
            messagebox.showwarning("Warning", "Cannot delete default admin")
            return
        if not messagebox.askyesno("Confirm", "Delete this user?"):
            return
        success, msg = self.db.delete_user(self.selected_username)
        if success:
            messagebox.showinfo("Success", msg)
            self.load_users()
        else:
            messagebox.showerror("Error", msg)

class UserForm:
    def __init__(self, parent, db, on_save=None):
        self.db = db
        self.on_save = on_save
        self.win = tk.Toplevel(parent)
        self.win.title("Add User")
        self.win.geometry("400x350")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.grab_set()
        self.build()

    def build(self):
        frame = ttk.Frame(self.win, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Username").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username = ttk.Entry(frame, width=30)
        self.username.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Password").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password = ttk.Entry(frame, show="*", width=30)
        self.password.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Role").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.role = ttk.Combobox(frame, values=["admin", "hr", "manager", "staff"], state="readonly", width=27)
        self.role.set("staff")
        self.role.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Employee ID (optional)").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.emp_id = ttk.Entry(frame, width=30)
        self.emp_id.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(frame, text="Save", command=self.save).grid(row=4, column=0, columnspan=2, pady=15)

    def save(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        role = self.role.get()
        emp_id = self.emp_id.get().strip() or None
        if not username or not password:
            messagebox.showerror("Error", "Username and Password are required")
            return
        success, msg = self.db.add_user(username, password, role, emp_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.win.destroy()
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror("Error", msg)
