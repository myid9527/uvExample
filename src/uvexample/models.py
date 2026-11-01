from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

# 这是 SQLAlchemy 声明式 ORM 的基础类。
# 后续所有需要映射到数据库的模型，都继承这个 Base。
class Base(DeclarativeBase):
    pass

class User(Base):
    # 表示这个 Python 类对应数据库中的 users 表。
    __tablename__ = "users"

    # Mapped[int]：告诉 SQLAlchemy，这个属性映射的是一个整数类型字段。
    # mapped_column(...)：定义数据库列的具体属性。
    # nullable=False：数据库不允许该列为 NULL。
    # primary_key=True：主键。
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)