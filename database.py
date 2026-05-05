import os
import pymysql
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

def get_connection():#获取数据库连接
    return pymysql.connect(**DB_CONFIG)

def init_db():  #初始化数据库，创建表
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists endings (
            id int auto_increment primary key,
            player_name varchar(50) not null,
            final_wealth int,
            final_skill int,
            final_health int,
            final_luck int,
            ending_text text,
            created_at timestamp default current_timestamp
        ) engine=innodb default charset=utf8mb4
    ''')
    conn.commit()
    cursor.close()
    conn.close()
        
def save_ending(player, ending_text):  #保存结局记录
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        insert into endings (player_name, final_wealth, final_skill, final_health, final_luck, ending_text)
        values (%s, %s, %s, %s, %s, %s)
    ''', (player.name, player.wealth, player.skill, player.health, player.luck, ending_text))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_endings(limit=10):  #获取所有结局记录
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        select player_name, final_wealth, final_skill, final_health, final_luck, ending_text, created_at
        from endings
        order by created_at desc
        limit %s
    ''', (limit,))
    rows = cursor.fetchall()#获取所有记录
    cursor.close()
    conn.close()
    return rows
