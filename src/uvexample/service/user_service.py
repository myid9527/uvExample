# 因为 Service 不属于 FastAPI 的 HTTP 接口层。

# Depends 是 FastAPI 的依赖注入机制，通常在 Router 等 FastAPI 管理的调用入口中使用。

# Service 应该保持普通 Python 函数的特性，由调用方主动传入依赖。


from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserCreate, UserUpdate


# 新增用户
def create_user(db: Session, user_data: UserCreate):
    db_user = User(
        username=user_data.username,
        age=user_data.age,
        full_name=user_data.full_name,
        email=str(user_data.email)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# 查询用户列表
def get_users(db: Session):
    statement = select(User)
    return db.scalars(statement).all()


# 查询单个用户
def get_user(db: Session, username: str):
    statement = select(User).where(
        User.username == username
    )

    return db.scalar(statement)


# 修改用户
def update_user(
    db: Session,
    username: str,
    user_data: UserUpdate
):
    user = get_user(db, username)

    if user is None:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


# 删除用户
def delete_user(db: Session, username: str):
    user = get_user(db, username)

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True