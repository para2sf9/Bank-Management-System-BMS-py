"""
Bank Database Service Layer
Wraps core.db_engine.DatabaseEngine with business-specific methods.
"""

from datetime import datetime
from core.db_engine import DatabaseEngine

class BankDatabase:
    def __init__(self):
        self.engine = DatabaseEngine()
        self.connected = self.engine.connected
        self.db = self.engine.db

    def authenticate(self, username, password):
        return self.engine.authenticate(username, password)

    def add_user(self, username, password, role, employee_id=None):
        return self.engine.add_user(username, password, role, employee_id)

    def get_users(self):
        return self.engine.get_users()

    def delete_user(self, username):
        return self.engine.delete_user(username)

    # Employees
    def add_employee(self, data):
        try:
            data["salary"] = float(data.get("salary", 0))
            self.engine.insert_one("employees", data)
            return True, "Employee added"
        except Exception as e:
            return False, str(e)

    def get_employees(self, search=None, department=None):
        query = {}
        if search:
            query["$or"] = [
                {"first_name": {"$regex": search, "$options": "i"}},
                {"last_name": {"$regex": search, "$options": "i"}},
                {"employee_id": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}}
            ]
        if department:
            query["department_id"] = department
        return self.engine.find("employees", query, limit=500, sort=[("last_name", 1), ("first_name", 1)])

    def get_employee_by_id(self, employee_id_str):
        return self.engine.find_one("employees", {"employee_id": employee_id_str})

    def update_employee(self, employee_id_str, data):
        try:
            data["salary"] = float(data.get("salary", 0))
            data["updated_at"] = datetime.now()
            self.engine.update_one("employees", {"employee_id": employee_id_str}, data)
            return True, "Updated"
        except Exception as e:
            return False, str(e)

    def delete_employee(self, employee_id_str):
        self.engine.soft_delete("employees", {"employee_id": employee_id_str})
        self.engine.hard_delete("users", {"employee_id": employee_id_str})
        return True, "Deleted (soft)"

    # Departments
    def add_department(self, data):
        try:
            self.engine.insert_one("departments", data)
            return True, "Added"
        except Exception as e:
            return False, str(e)

    def get_departments(self):
        return self.engine.find("departments", {}, limit=500)

    def get_department_by_id(self, dept_id_str):
        return self.engine.find_one("departments", {"department_id": dept_id_str})

    def update_department(self, dept_id_str, data):
        self.engine.update_one("departments", {"department_id": dept_id_str}, data)
        return True, "Updated"

    def delete_department(self, dept_id_str):
        self.engine.hard_delete("departments", {"department_id": dept_id_str})
        return True, "Deleted"

    # Attendance
    def mark_attendance(self, data):
        try:
            parts = data["date"].split("-")
            data["month"] = int(parts[1])
            data["year"] = int(parts[0])
            existing = self.engine.find_one("attendance", {"employee_id": data["employee_id"], "date": data["date"]})
            if existing:
                self.engine.update_one("attendance", {"employee_id": data["employee_id"], "date": data["date"]}, data)
                return True, "Attendance updated"
            else:
                self.engine.insert_one("attendance", data)
                return True, "Attendance marked"
        except Exception as e:
            return False, str(e)

    def get_attendance(self, month=None, year=None, date=None):
        query = {}
        if month is not None:
            query["month"] = month
        if year is not None:
            query["year"] = year
        if date:
            query["date"] = date
        return self.engine.find("attendance", query, limit=1000, sort=[("date", -1)])

    # Payroll
    def generate_payroll(self, data):
        try:
            data["net_salary"] = data["base_salary"] + data.get("bonus", 0) - data.get("deductions", 0)
            data["generated_at"] = datetime.now()
            existing = self.engine.find_one("payroll", {
                "employee_id": data["employee_id"],
                "month": data["month"],
                "year": data["year"]
            })
            if existing:
                self.engine.update_one("payroll", {
                    "employee_id": data["employee_id"],
                    "month": data["month"],
                    "year": data["year"]
                }, data)
                return True, "Payroll updated"
            else:
                self.engine.insert_one("payroll", data)
                return True, "Payroll generated"
        except Exception as e:
            return False, str(e)

    def get_payroll(self, month=None, year=None):
        query = {}
        if month is not None:
            query["month"] = month
        if year is not None:
            query["year"] = year
        return self.engine.find("payroll", query, limit=1000, sort=[("year", -1), ("month", -1)])

    # Branches
    def add_branch(self, data):
        try:
            self.engine.insert_one("branches", data)
            return True, "Branch added"
        except Exception as e:
            return False, str(e)

    def get_branches(self):
        return self.engine.find("branches", {}, limit=500)

    def get_branch_by_id(self, branch_id_str):
        return self.engine.find_one("branches", {"branch_id": branch_id_str})

    def update_branch(self, branch_id_str, data):
        self.engine.update_one("branches", {"branch_id": branch_id_str}, data)
        return True, "Updated"

    def delete_branch(self, branch_id_str):
        self.engine.hard_delete("branches", {"branch_id": branch_id_str})
        return True, "Deleted"

    # Leaves
    def add_leave(self, data):
        try:
            self.engine.insert_one("leaves", data)
            return True, "Leave added"
        except Exception as e:
            return False, str(e)

    def get_leaves(self, employee_id=None, status=None):
        query = {}
        if employee_id:
            query["employee_id"] = employee_id
        if status:
            query["status"] = status
        return self.engine.find("leaves", query, limit=500, sort=[("start_date", -1)])

    def update_leave(self, leave_id, data):
        from bson.objectid import ObjectId
        self.engine.update_one("leaves", {"_id": ObjectId(leave_id)}, data)
        return True, "Updated"

    def delete_leave(self, leave_id):
        from bson.objectid import ObjectId
        self.engine.hard_delete("leaves", {"_id": ObjectId(leave_id)})
        return True, "Deleted"

    # Audit logs
    def get_audit_logs(self, limit=500):
        return list(self.engine.db.audit_logs.find().sort("timestamp", -1).limit(limit))

    # Stats
    def get_stats(self):
        return self.engine.get_stats()

    def get_employee_names_map(self):
        return self.engine.get_employee_names_map()
