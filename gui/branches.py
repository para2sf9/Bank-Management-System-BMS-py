import tkinter as tk
from tkinter import ttk, messagebox

class BranchesView:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.selected_branch_id = None
        self.build()

    def build(self):
        ttk.Label(self.parent, text="Branches", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.parent)
        top.pack(fill="x", pady=5)
        ttk.Button(top, text="Refresh", command=self.load_branches).pack(side="left", padx=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(top, text="Add Branch", command=self.open_add_window).pack(side="right", padx=5)

        cols = ("Branch ID", "Name", "Address", "City", "Phone", "Manager ID")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=170, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill="x", pady=5)
        if self.user.get("role") in ("admin", "hr"):
            ttk.Button(btn_frame, text="Edit", command=self.open_edit_window).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Delete", command=self.delete_branch).pack(side="left", padx=5)

        self.load_branches()

    def load_branches(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for b in self.db.get_branches():
            self.tree.insert("", "end", iid=b["branch_id"], values=(
                b.get("branch_id", ""),
                b.get("name", ""),
                b.get("address", ""),
                b.get("city", ""),
                b.get("phone", ""),
                b.get("manager_id", "") or ""
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_branch_id = selected[0]

    def open_add_window(self):
        BranchForm(self.parent, self.db, on_save=self.load_branches)

    def open_edit_window(self):
        if not self.selected_branch_id:
            messagebox.showwarning("Warning", "Select a branch first")
            return
        branch = self.db.get_branch_by_id(self.selected_branch_id)
        if not branch:
            messagebox.showerror("Error", "Branch not found")
            return
        BranchForm(self.parent, self.db, branch=branch, on_save=self.load_branches)

    def delete_branch(self):
        if not self.selected_branch_id:
            messagebox.showwarning("Warning", "Select a branch first")
            return
        if not messagebox.askyesno("Confirm", "Delete this branch?"):
            return
        success, msg = self.db.delete_branch(self.selected_branch_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.load_branches()
        else:
            messagebox.showerror("Error", msg)

class BranchForm:
    def __init__(self, parent, db, branch=None, on_save=None):
        self.db = db
        self.branch = branch
        self.on_save = on_save
        self.win = tk.Toplevel(parent)
        self.win.title("Edit Branch" if branch else "Add Branch")
        self.win.geometry("450x400")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.win.grab_set()
        self.build()

    def build(self):
        frame = ttk.Frame(self.win, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Branch ID").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.branch_id = ttk.Entry(frame, width=30)
        self.branch_id.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Name").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name = ttk.Entry(frame, width=30)
        self.name.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Address").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.address = ttk.Entry(frame, width=30)
        self.address.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="City").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.city = ttk.Entry(frame, width=30)
        self.city.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Phone").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.phone = ttk.Entry(frame, width=30)
        self.phone.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Manager Employee ID").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.manager = ttk.Entry(frame, width=30)
        self.manager.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(frame, text="Save", command=self.save).grid(row=6, column=0, columnspan=2, pady=15)

        if self.branch:
            self.branch_id.insert(0, self.branch.get("branch_id", ""))
            self.branch_id.config(state="disabled")
            self.name.insert(0, self.branch.get("name", ""))
            self.address.insert(0, self.branch.get("address", ""))
            self.city.insert(0, self.branch.get("city", ""))
            self.phone.insert(0, self.branch.get("phone", ""))
            self.manager.insert(0, self.branch.get("manager_id", "") or "")

    def save(self):
        data = {
            "branch_id": self.branch_id.get().strip(),
            "name": self.name.get().strip(),
            "address": self.address.get().strip(),
            "city": self.city.get().strip(),
            "phone": self.phone.get().strip(),
            "manager_id": self.manager.get().strip() or None
        }
        if not data["branch_id"] or not data["name"]:
            messagebox.showerror("Error", "Branch ID and Name are required")
            return
        if self.branch:
            success, msg = self.db.update_branch(data["branch_id"], data)
        else:
            success, msg = self.db.add_branch(data)
        if success:
            messagebox.showinfo("Success", msg)
            self.win.destroy()
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror("Error", msg)
