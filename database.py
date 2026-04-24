import os
import pymysql
from dotenv import load_dotenv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('MYSQLHOST'),
    'port': int(os.getenv('MYSQLPORT', 3306)),
    'user': os.getenv('MYSQLUSER'),
    'password': os.getenv('MYSQLPASSWORD'),
    'database': os.getenv('MYSQLDATABASE'),
    'charset': 'utf8mb4'
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def init_db():  #初始化数据库，创建表
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS endings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_name VARCHAR(50) NOT NULL,
            final_wealth INT,
            final_skill INT,
            final_health INT,
            final_luck INT,
            ending_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    conn.commit()
    cursor.close()
    conn.close()
        
def save_ending(player, ending_text):  #保存结局记录
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO endings (player_name, final_wealth, final_skill, final_health, final_luck, ending_text)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (player.name, player.wealth, player.skill, player.health, player.luck, ending_text))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_endings(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_name, final_wealth, final_skill, final_health, final_luck, ending_text, created_at
        FROM endings
        ORDER BY created_at DESC
        LIMIT %s
    ''', (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
