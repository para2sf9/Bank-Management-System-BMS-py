import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, root, db, on_login):
        self.root = root
        self.db = db
        self.on_login = on_login
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        self.build()

    def build(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Bank Management System", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Username").grid(row=1, column=0, sticky="w", pady=5)
        self.user_entry = ttk.Entry(frame, width=25)
        self.user_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Password").grid(row=2, column=0, sticky="w", pady=5)
        self.pass_entry = ttk.Entry(frame, show="*", width=25)
        self.pass_entry.grid(row=2, column=1, pady=5)

        ttk.Button(frame, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=15)

        if not self.db.connected:
            ttk.Label(frame, text="Warning: MongoDB not connected", foreground="red").grid(row=4, column=0, columnspan=2)

        self.user_entry.bind("<Return>", lambda e: self.login())
        self.pass_entry.bind("<Return>", lambda e: self.login())

    def login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Enter username and password")
            return
        user = self.db.authenticate(username, password)
        if user:
            self.root.destroy()
            self.on_login(user)
        else:
            messagebox.showerror("Error", "Invalid credentials")
