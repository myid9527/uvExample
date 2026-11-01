from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from .database import get_db
from .models import User
from .schemas import UserCreate, UserResponse
app = FastAPI()

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username, 
        age=user.age,
        full_name=user.full_name,
        email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{username}")
def read_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return {"error": "User not found"}
    return user

@app.get("/users",response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    # 构建查询语句，还没有真正执行查询。
    statements = select(User)
    # 执行查询，返回一个结果对象。
    results = db.execute(statements)
    # - scalars()：从结果中提取每行的第一个元素，也就是 User ORM 对象。
    # - all()：获取所有结果。
    # 最终得到的是一个 Python 列表，里面每个元素都是 User 对象。
    users = results.scalars().all()
    # 是 Python 列表推导式。

    # 和你熟悉的 JavaScript非常相似。：
    # users.map(user => ({
    # id: user.id,
    # username: user.username
    # }))
    return [
        {
            "id": user.id,
            "username": user.username,
            "age": user.age,
            "full_name": user.full_name,
            "email": user.email
        }
        for user in users
    ]

@app.patch("/users/{username}")
def update_user(username: str, user_update: UserCreate, db: Session = Depends(get_db)):
    # 1. 查询用户
    statement = select(User).where(User.username == username)

    user = db.scalar(statement)
    # 2. 检查用户是否存在
    if user is None:
        return {"error": "User not found"}

    # 3. 获取请求中实际传入的字段 使用 exclude_unset=True 只更新传入的字段
    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        return {"error": "No fields to update"}

    for key, value in update_data.items():
        # 它的作用是动态设置对象属性。setattr(user, "age", 20) == user.age = 20
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


    # user = db.query(User).filter(User.username == username).first()
    # if user is None:
    #     return {"error": "User not found"}

    # # 使用 exclude_unset=True 只更新传入的字段
    # update_data = user_update.model_dump(exclude_unset=True)
    # for key, value in update_data.items():
    #     setattr(user, key, value)
    
    # db.commit()
    # db.refresh(user)
    # return user

@app.delete("/users/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    statement = select(User).where(User.username == username)
    user = db.scalar(statement)
    if user is None:
        return {"error": "User not found"}
    
    db.delete(user)
    db.commit()
    return {"message": f"User '{username}' deleted successfully"}