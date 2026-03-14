import mysql.connector
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Default connection settings if not in Django settings
DB_CONFIG = getattr(settings, 'MYSQL_DB_CONFIG', {
    'host': 'localhost',
    'user': 'root',
    'password': 'Manad@2007',  # Update with your local MySQL root password
    'database': 'presence_pulse',
})

def get_connection(use_database=True):
    """
    Returns a MySQL connection. If use_database is False, connects without selecting
    a specific database (useful for initial DB creation).
    """
    config = DB_CONFIG.copy()
    if not use_database:
        config.pop('database', None)
        
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to MySQL: {err}")
        return None

def init_db():
    """
    Creates the database and users table if they don't exist.
    Call this once when the server starts.
    """
    # 1. Connect without DB to create the DB if needed
    conn = get_connection(use_database=False)
    if not conn:
        logger.error("Failed to connect to MySQL server. Ensure it is running.")
        return False
        
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.commit()
    except mysql.connector.Error as err:
        logger.error(f"Failed creating database: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    # 2. Connect to the DB to create tables
    conn = get_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                role VARCHAR(50) NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        logger.error(f"Failed creating tables: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
