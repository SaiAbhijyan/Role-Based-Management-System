import psycopg2

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postadmin",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establish connection to PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)
