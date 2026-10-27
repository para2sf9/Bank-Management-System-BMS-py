import tkinter as tk
from database import BankDatabase
from gui.login_window import LoginWindow
from gui.main_app import MainApp

def main():
    db = BankDatabase()

    def on_login(user):
        root = tk.Tk()
        root.title("Bank Management System")
        MainApp(root, user, db)
        root.mainloop()

    login_root = tk.Tk()
    login_root.title("Bank Management System - Login")
    LoginWindow(login_root, db, on_login)
    login_root.mainloop()

if __name__ == "__main__":
    main()
