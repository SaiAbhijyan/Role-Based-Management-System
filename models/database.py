import psycopg2

DB_CONFIG = {
    "dbname": "your_dbname",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establish connection to PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)
