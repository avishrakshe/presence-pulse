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
    Creates the database and unified users table if they don't exist.
    All data (signup + daily schedule + social media goals) stored in one table.
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

    # 2. Connect to the DB to create the unified table
    conn = get_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                
                -- Signup fields
                role VARCHAR(50) NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                
                -- Daily schedule fields
                wake_time TIME DEFAULT NULL,
                work_start TIME DEFAULT NULL,
                work_end TIME DEFAULT NULL,
                lunch_time TIME DEFAULT NULL,
                dinner_time TIME DEFAULT NULL,
                bed_time TIME DEFAULT NULL,
                exercise_time TIME DEFAULT NULL,
                no_phone_meals TINYINT DEFAULT 0,
                no_phone_bedtime TINYINT DEFAULT 0,
                no_phone_exercise TINYINT DEFAULT 0,
                
                -- Social media goals (minutes per day for each platform)
                sm_instagram INT DEFAULT 0,
                sm_twitter INT DEFAULT 0,
                sm_facebook INT DEFAULT 0,
                sm_tiktok INT DEFAULT 0,
                sm_youtube INT DEFAULT 0,
                sm_whatsapp INT DEFAULT 0,
                sm_snapchat INT DEFAULT 0,
                sm_reddit INT DEFAULT 0,
                notify_on_exceed TINYINT DEFAULT 1,
                weekend_relaxed TINYINT DEFAULT 0,
                
                -- Presence points
                presence_points INT DEFAULT 740,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Challenge responses log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenge_responses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_email VARCHAR(255) NOT NULL,
                challenge_name VARCHAR(255) NOT NULL,
                trigger_reason VARCHAR(255),
                action ENUM('accept', 'reject') NOT NULL,
                points_change INT NOT NULL,
                responded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_user_email (user_email)
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
