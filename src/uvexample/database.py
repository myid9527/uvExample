# Engine：数据库连接管理入口，负责管理连接池和数据库方言。
# Session：一次数据库操作的工作会话，负责跟踪对象、执行查询和管理事务。
# Model：描述数据库表结构。

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# 告诉 SQLAlchemy：
# - 使用 SQLite 数据库。
# - 数据库文件叫 users.db。
# - 文件位于当前工作目录下的相对路径
DATABASE_URL = "sqlite:///./data/users.db"


# create_engine() 通常不会立即建立实际数据库连接，而是在第一次需要连接时才获取连接。
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# bind=engine	告诉 Session 使用哪个数据库 Engine
# autoflush=False	不自动在查询前 Flush
# autocommit=False	不自动提交事务
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    # yield 关键字：把函数变成一个生成器，允许在函数中间暂停和恢复执行。
    # 在 FastAPI 中，yield 用于依赖注入，提供资源给请求处理函数使用。
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from .models import Base
# Base：所有 SQLAlchemy 模型的基础类。
# metadata：保存所有已注册模型的表结构信息。
# create_all()：检查这些表是否存在，不存在就创建。
# bind=engine：告诉它在哪个数据库中创建
Base.metadata.create_all(bind=engine)  # 创建所有表


