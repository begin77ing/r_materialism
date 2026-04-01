import mysql.connector

# MySQLに接続
conn = mysql.connector.connect(
    host="localhost",
    user="akira",
    password="dounimonarannZ78",
    database="r_materialism"
)

# カーソルを取得
cursor = conn.cursor()

# テーブル作成のクエリ
create_table_query = """
CREATE TABLE IF NOT EXISTS option_info (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    command_string TEXT,
    family_name TEXT,
    family_number INT
)
"""

# テーブル作成
cursor.execute(create_table_query)
conn.commit()

# 接続を閉じる
cursor.close()
conn.close()