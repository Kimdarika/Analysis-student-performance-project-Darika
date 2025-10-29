# config.py
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'performance_db'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)