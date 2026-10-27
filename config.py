MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bank_management_system"

# Advanced connection pool settings
MONGO_OPTIONS = {
    "maxPoolSize": 50,
    "minPoolSize": 10,
    "maxIdleTimeMS": 45000,
    "serverSelectionTimeoutMS": 5000,
    "socketTimeoutMS": 5000,
    "connectTimeoutMS": 10000,
    "retryWrites": True,
}
