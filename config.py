# config.py
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'student_managerment_db'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)