"""
Reset Admin User Script
Run this if you get "Invalid credentials" even with correct password.
Requires MongoDB to be running.
"""

from pymongo import MongoClient
import hashlib
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bank_management_system"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[DB_NAME]

        # Remove existing admin if any
        db.users.delete_one({"username": "admin"})

        # Insert fresh admin
        db.users.insert_one({
            "username": "admin",
            "password_hash": hash_password("admin123"),
            "role": "admin",
            "employee_id": None,
            "created_at": datetime.now(),
            "is_active": True,
            "is_deleted": False
        })

        print("Admin user reset successfully!")
        print("Username: admin")
        print("Password: admin123")
    except Exception as e:
        print("Error:", e)
        print("Make sure MongoDB is running before executing this script.")

if __name__ == "__main__":
    main()
