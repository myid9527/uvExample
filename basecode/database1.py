import sqlite3
from pathlib import Path

# database.py → uvexample → src → 项目根目录
project_root = Path(__file__).resolve().parents[2]
db_path = project_root / "data" / "users.db"

db_path.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(db_path)

conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        age INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL
    )
""")

conn.commit();
conn.close();


def get_db_connection():
    conn = sqlite3.connect(db_path,check_same_thread=False)
    conn.row_factory = sqlite3.Row  # 设置行工厂，使查询结果以字典形式返回
    try:
        #yield conn：把连接提供给接口使用；接口执行完成后，FastAPI 会继续执行 finally，关闭连接。
        yield conn;
    finally:
        conn.close()