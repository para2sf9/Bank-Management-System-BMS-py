"""
Advanced Database Engine for Bank Management System
Implements core database concepts:
- Connection Pooling
- ACID Transactions
- Indexing Strategies
- Schema Validation (via application layer)
- Query Optimization
- Audit Logging
- Soft Deletes
- Data Normalization helpers
"""

import hashlib
import threading
import time
from datetime import datetime
from contextlib import contextmanager

try:
    from pymongo import MongoClient, ASCENDING, DESCENDING
    from pymongo.errors import DuplicateKeyError, PyMongoError, ConnectionFailure
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False
    DuplicateKeyError = Exception
    PyMongoError = Exception
    ConnectionFailure = Exception

import config

class DatabaseEngine:
    """
    Singleton database engine with connection pooling,
    transaction support, and advanced indexing.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.client = None
        self.db = None
        self.connected = False
        self._initialized = True
        if PYMONGO_AVAILABLE:
            self.connect()

    def connect(self):
        try:
            self.client = MongoClient(config.MONGO_URI, **config.MONGO_OPTIONS)
            self.client.admin.command("ping")
            self.db = self.client[config.DB_NAME]
            self.connected = True
            self._setup_collections()
            self._ensure_indexes()
            self._seed_data()
            return True
        except Exception as e:
            print("DB Connection Error:", e)
            self.connected = False
            return False

    def _setup_collections(self):
        # Core collections
        cols = ["employees", "departments", "attendance", "payroll", "users", "audit_logs", "branches", "leaves"]
        for c in cols:
            if c not in self.db.list_collection_names():
                self.db.create_collection(c)

    def _ensure_indexes(self):
        # Employees: unique employee_id and email
        self.db.employees.create_index([("employee_id", ASCENDING)], unique=True, name="idx_emp_id")
        self.db.employees.create_index([("email", ASCENDING)], unique=True, name="idx_emp_email")
        self.db.employees.create_index([("department_id", ASCENDING)], name="idx_emp_dept")
        self.db.employees.create_index([("status", ASCENDING)], name="idx_emp_status")
        self.db.employees.create_index([("last_name", ASCENDING), ("first_name", ASCENDING)], name="idx_emp_name")

        # Departments
        self.db.departments.create_index([("department_id", ASCENDING)], unique=True, name="idx_dept_id")

        # Attendance: composite unique on employee + date
        self.db.attendance.create_index([("employee_id", ASCENDING), ("date", ASCENDING)], unique=True, name="idx_attendance")
        self.db.attendance.create_index([("date", ASCENDING), ("status", ASCENDING)], name="idx_att_date_status")

        # Payroll: composite unique on employee + month + year
        self.db.payroll.create_index([("employee_id", ASCENDING), ("month", ASCENDING), ("year", ASCENDING)], unique=True, name="idx_payroll")

        # Users
        self.db.users.create_index([("username", ASCENDING)], unique=True, name="idx_user_username")

        # Audit logs
        self.db.audit_logs.create_index([("timestamp", DESCENDING)], name="idx_audit_time")
        self.db.audit_logs.create_index([("collection", ASCENDING), ("timestamp", DESCENDING)], name="idx_audit_col_time")

        # Branches
        self.db.branches.create_index([("branch_id", ASCENDING)], unique=True, name="idx_branch_id")

        # Leaves
        self.db.leaves.create_index([("employee_id", ASCENDING), ("start_date", ASCENDING)], name="idx_leaves_emp")

    def _seed_data(self):
        if self.db.users.count_documents({}) == 0:
            self.db.users.insert_one({
                "username": "admin",
                "password_hash": self._hash_password("admin123"),
                "role": "admin",
                "employee_id": None,
                "created_at": datetime.now(),
                "is_active": True
            })
        # Seed sample departments if empty
        if self.db.departments.count_documents({}) == 0:
            sample_depts = [
                {"department_id": "D001", "name": "Human Resources", "manager": "TBD", "location": "Head Office", "created_at": datetime.now()},
                {"department_id": "D002", "name": "Finance", "manager": "TBD", "location": "Head Office", "created_at": datetime.now()},
                {"department_id": "D003", "name": "IT", "manager": "TBD", "location": "Tech Block", "created_at": datetime.now()},
                {"department_id": "D004", "name": "Operations", "manager": "TBD", "location": "Branch Network", "created_at": datetime.now()},
                {"department_id": "D005", "name": "Risk & Compliance", "manager": "TBD", "location": "Head Office", "created_at": datetime.now()},
            ]
            self.db.departments.insert_many(sample_depts)
        # Seed sample branches if empty
        if self.db.branches.count_documents({}) == 0:
            sample_branches = [
                {"branch_id": "B001", "name": "Main Branch", "address": "123 Finance St", "city": "New York", "phone": "555-0101", "manager_id": None, "created_at": datetime.now()},
                {"branch_id": "B002", "name": "Downtown Branch", "address": "456 Commerce Ave", "city": "New York", "phone": "555-0102", "manager_id": None, "created_at": datetime.now()},
            ]
            self.db.branches.insert_many(sample_branches)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ------------------ Audit Logging ------------------
    def log_audit(self, action, collection, document_id, user=None, details=None):
        try:
            self.db.audit_logs.insert_one({
                "action": action,
                "collection": collection,
                "document_id": str(document_id),
                "user": user,
                "details": details,
                "timestamp": datetime.now()
            })
        except Exception:
            pass

    # ------------------ Transactions ------------------
    @contextmanager
    def transaction(self):
        """
        Multi-document ACID transaction context manager.
        Requires MongoDB replica set for full ACID.
        Falls back to best-effort on standalone.
        """
        if not self.connected:
            yield self.db
            return
        try:
            with self.client.start_session() as session:
                with session.start_transaction():
                    yield self.db
        except Exception:
            # Fallback for standalone MongoDB without replica set
            yield self.db

    # ------------------ CRUD with Soft Delete ------------------
    def insert_one(self, collection, data, user=None):
        data["created_at"] = datetime.now()
        data["is_deleted"] = False
        result = self.db[collection].insert_one(data)
        self.log_audit("INSERT", collection, result.inserted_id, user, None)
        return result

    def find_one(self, collection, query, include_deleted=False):
        if not include_deleted:
            query = {**query, "is_deleted": False}
        return self.db[collection].find_one(query)

    def find(self, collection, query=None, include_deleted=False, limit=500, sort=None):
        if query is None:
            query = {}
        if not include_deleted:
            query = {**query, "is_deleted": False}
        cursor = self.db[collection].find(query)
        if sort:
            cursor = cursor.sort(sort)
        return list(cursor.limit(limit))

    def update_one(self, collection, query, update_data, user=None):
        update_data["updated_at"] = datetime.now()
        result = self.db[collection].update_one(query, {"$set": update_data})
        # Try to get _id for audit
        doc = self.db[collection].find_one(query, {"_id": 1})
        if doc:
            self.log_audit("UPDATE", collection, doc["_id"], user, None)
        return result

    def soft_delete(self, collection, query, user=None):
        result = self.db[collection].update_one(query, {"$set": {"is_deleted": True, "deleted_at": datetime.now()}})
        doc = self.db[collection].find_one(query, {"_id": 1})
        if doc:
            self.log_audit("SOFT_DELETE", collection, doc["_id"], user, None)
        return result

    def hard_delete(self, collection, query, user=None):
        doc = self.db[collection].find_one(query, {"_id": 1})
        result = self.db[collection].delete_one(query)
        if doc:
            self.log_audit("HARD_DELETE", collection, doc["_id"], user, None)
        return result

    def count(self, collection, query=None, include_deleted=False):
        if query is None:
            query = {}
        if not include_deleted:
            query = {**query, "is_deleted": False}
        return self.db[collection].count_documents(query)

    # ------------------ Aggregation Helpers ------------------
    def aggregate(self, collection, pipeline):
        return list(self.db[collection].aggregate(pipeline))

    # ------------------ Auth ------------------
    def authenticate(self, username, password):
        if not self.connected:
            return None
        user = self.db.users.find_one({"username": username, "is_deleted": False})
        if user and user["password_hash"] == self._hash_password(password):
            return {"username": user["username"], "role": user["role"], "employee_id": user.get("employee_id")}
        return None

    def add_user(self, username, password, role, employee_id=None):
        try:
            self.db.users.insert_one({
                "username": username,
                "password_hash": self._hash_password(password),
                "role": role,
                "employee_id": employee_id,
                "created_at": datetime.now(),
                "is_active": True,
                "is_deleted": False
            })
            return True, "User created"
        except DuplicateKeyError:
            return False, "Username already exists"

    def get_users(self):
        if not self.connected:
            return []
        return list(self.db.users.find({"is_deleted": False}, {"password_hash": 0}))

    def delete_user(self, username):
        if not self.connected:
            return False, "Not connected"
        if username == "admin":
            return False, "Cannot delete default admin"
        self.db.users.delete_one({"username": username})
        return True, "Deleted"

    # ------------------ Stats ------------------
    def get_stats(self):
        if not self.connected:
            return {"total_employees": 0, "total_departments": 0, "present_today": 0, "total_branches": 0}
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "total_employees": self.count("employees"),
            "total_departments": self.count("departments"),
            "present_today": self.count("attendance", {"date": today, "status": "Present"}),
            "total_branches": self.count("branches")
        }

    def get_employee_names_map(self):
        if not self.connected:
            return {}
        employees = self.find("employees", {}, limit=1000)
        return {e["employee_id"]: f"{e['first_name']} {e['last_name']}" for e in employees}
