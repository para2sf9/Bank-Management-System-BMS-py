# Bank Management System

A desktop GUI application for managing bank internal operations including employees, departments, attendance, payroll, branches, leaves, and audit logs.<br/>
<img width="1197" height="718" alt="image" src="https://github.com/user-attachments/assets/8a472e2f-5149-4bab-9fae-f837dfa2f642" />
<img width="399" height="348" alt="image" src="https://github.com/user-attachments/assets/0c9ac575-6cfa-48e2-b308-60c1f44d488a" /><br/>
<img width="1197" height="718" alt="image" src="https://github.com/user-attachments/assets/cb5bb3df-2cfe-472c-819d-ffea8eec147e" /><br/>
<img width="1193" height="667" alt="image" src="https://github.com/user-attachments/assets/43da8504-dad4-4354-afd5-2b3602956274" /><br/>
<img width="1366" height="729" alt="image" src="https://github.com/user-attachments/assets/ddbb40a6-177e-4c16-a8ca-cac7a38547fe" /><br/>
<img width="1366" height="720" alt="image" src="https://github.com/user-attachments/assets/b32a7ce2-a846-46e5-937e-be9d6854be4d" /><br/>
<img width="1364" height="725" alt="image" src="https://github.com/user-attachments/assets/21377754-e6dc-4dc4-8f04-ecee726b8875" /><br/>
<img width="1366" height="724" alt="image" src="https://github.com/user-attachments/assets/0371a1c8-a0e9-41e3-9818-29a5c95dd567" /><br/>
<img width="1366" height="723" alt="image" src="https://github.com/user-attachments/assets/14308f2d-f49d-44a8-9834-dfbdcb506cc9" /><br/>
<img width="1363" height="722" alt="image" src="https://github.com/user-attachments/assets/a19abd3e-5d22-414e-94e9-7c26fa309350" /><br/>
<img width="1366" height="725" alt="image" src="https://github.com/user-attachments/assets/6fe94297-fe03-4655-862e-4fc0a7f2f96e" /><br/>
<img width="1366" height="721" alt="image" src="https://github.com/user-attachments/assets/c0ec3ca4-4a29-4a4c-bcb8-2a63308abd05" /><br/>
<img width="1366" height="725" alt="image" src="https://github.com/user-attachments/assets/093e798c-afc2-4093-93b7-b573df5ab928" /><br/>

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
