"""
Diagnose MongoDB connection and admin user existence.
"""

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bank_management_system"

def main():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("MongoDB Connection: OK")
        db = client[DB_NAME]
        user = db.users.find_one({"username": "admin"})
        if user:
            print("Admin user exists: YES")
            print("Role:", user.get("role"))
            print("Is active:", user.get("is_active"))
            print("Is deleted:", user.get("is_deleted"))
        else:
            print("Admin user exists: NO")
            print("Run: python reset_admin.py")
    except Exception as e:
        print("MongoDB Connection: FAILED")
        print("Error:", e)

if __name__ == "__main__":
    main()
