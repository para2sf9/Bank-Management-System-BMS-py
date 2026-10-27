# Advanced Database Concepts in Bank Management System

## 1. Connection Pooling
- MongoClient is created as a singleton with configurable pool sizes (`maxPoolSize=50`, `minPoolSize=10`).
- This avoids creating a new connection for every operation, improving performance and reducing latency.

## 2. ACID Transactions
- The `DatabaseEngine.transaction()` context manager wraps multi-document operations in a session.
- MongoDB supports ACID transactions when running as a replica set.
- On standalone MongoDB, it gracefully falls back to best-effort consistency.

## 3. Indexing Strategy
- Unique indexes on `employee_id`, `email`, `department_id`, `branch_id`, and `username` enforce data integrity.
- Composite indexes on `attendance` (employee + date) and `payroll` (employee + month + year) optimize lookups.
- Covered queries and sorted retrieval are supported via `last_name`, `first_name`, `status`, and `timestamp` indexes.

## 4. Soft Deletes
- Records are not permanently removed. Instead, `is_deleted=True` and `deleted_at` timestamp are set.
- Queries automatically filter out soft-deleted documents unless explicitly requested.
- This supports data recovery, audit trails, and referential safety.

## 5. Audit Logging
- Every INSERT, UPDATE, SOFT_DELETE, and HARD_DELETE is recorded in the `audit_logs` collection.
- Fields: action, collection, document_id, user, timestamp, details.
- Helps with compliance, debugging, and traceability.

## 6. Aggregation Framework
- The engine exposes an `aggregate()` method for complex analytics.
- Example use cases: department-wise headcount, monthly attendance summaries, payroll reports.

## 7. Schema Validation (Application Layer)
- Although MongoDB is schemaless, the application enforces required fields and data types.
- Salary, bonus, and deductions are coerced to floats. Dates are validated as strings in YYYY-MM-DD format.

## 8. Data Normalization vs Denormalization
- Employees reference departments and branches by ID (normalized) to avoid duplication.
- Employee names are cached in memory for display purposes (light denormalization) to reduce joins.

## 9. Role-Based Access Control (RBAC)
- Users collection stores roles: admin, hr, manager, staff.
- GUI views restrict add/edit/delete buttons based on the logged-in user role.
- Admin has full access; HR manages employees, attendance, payroll, and branches; Managers and Staff have read access.

## 10. Backup & Recovery Considerations
- MongoDB provides `mongodump` and `mongorestore` for backups.
- Soft deletes and audit logs provide an additional safety net before hard deletion.
