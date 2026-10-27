# Bank Management System

A desktop GUI application for managing bank internal operations including employees, departments, attendance, payroll, branches, leaves, and audit logs.

## Features
- Employee Management (CRUD with soft delete)
- Department Management
- Attendance Tracking
- Payroll Generation
- Branch Management
- Leave Management
- Audit Logs
- Role-based Access (Admin, HR, Manager, Staff)
- Dashboard with Statistics
- Advanced Database Concepts implemented (Connection Pooling, ACID Transactions, Indexing, Soft Deletes, Aggregation)

## Requirements
- Python 3.8+
- MongoDB 4.4+ (local or remote)

## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure MongoDB is running:
   ```
   mongod
   ```

3. Run the application:
   ```
   python run.py
   ```
   Or on Windows:
   ```
   run.bat
   ```

## Default Login
- Username: `admin`
- Password: `admin123`

## Notes
- MongoDB connection string can be modified in `config.py`
- Default connection: `mongodb://localhost:27017/`
- See `docs/database_concepts.md` for detailed database design notes.
