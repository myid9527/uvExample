import sqlite3
from fastapi import FastAPI, Depends
from pydantic import BaseModel,ConfigDict
from basecode.database1 import get_db_connection
class User(BaseModel):
    # 严格模式,检查模型属性，不开启的话，age：“18” 会转成18，
    model_config = ConfigDict(strict=True)
    # None = None 也就是可选类型，默认值为None,如果不设置默认值，代表参数还是必选，只不过可以接受None
    username: str | None = None
    age: int | None = None
    full_name: str | None = None
    email: str | None = None

app = FastAPI()

@app.get("/user")
def get_users(conn: sqlite3.Connection = Depends(get_db_connection)):
    # cursor 可以理解为数据库操作的结果对象。
    cursor = conn.execute("SELECT * FROM users")
    # fetchall() 表示获取查询结果中剩余的所有行。
    users = cursor.fetchall()
    # return {"users": users}
    #返回结果{
        #   "users": [
        #     [1, "tom", 18, "Tom Smith", "tom@example.com"],
        #     [2, "jack", 25, "Jack Smith", "jack@example.com"]
        #   ]
        # }
    # 由于我们在 get_db_connection() 中设置了行工厂为 sqlite3.Row，所以查询结果是一个 Row 对象的列表。
    # Row 对象可以像字典一样访问列名，所以我们可以将每一行转换为字典。
    users_dict = [dict(user) for user in users]
    return {"users": users_dict}

@app.post("/user")
def create_user(user: User,conn: sqlite3.Connection = Depends(get_db_connection)): 
    # Depends(get_db_connection)：告诉 FastAPI，执行接口前先调用 get_db()，把获取到的连接传给 conn。
    
    cursor = conn.execute(
        """
        INSERT INTO users (username, age, full_name, email)
        VALUES (?, ?, ?, ?)
        """,
        (
            user.username,
            user.age,
            user.full_name,
            user.email
        )
    );

    conn.commit();
    user_id = cursor.lastrowid;
    return {"user_id": user_id, "user": user.model_dump()};

@app.patch("/user/{username}/age")
def update_user_age(username: str, age: int, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.execute(
        """
        UPDATE users
        SET age = ?
        WHERE username = ?
        """,
        (age, username)
    )
    conn.commit()
    if cursor.rowcount == 0:
        return {"message": f"No user found with username '{username}'."}
    return {"message": f"User '{username}' age updated to {age}."}

@app.patch("/user/{username}")
def update_user(username: str, user: User, conn: sqlite3.Connection = Depends(get_db_connection)):
    updata_data = user.model_dump(exclude_unset=True)
    if not updata_data:
        return {"message": "No fields to update."}
    set_clause = ",".join(f"{key} = ?" for key in updata_data)
    values = list(updata_data.values())
    values.append(username)  # 添加 username 到参数列表
    cursor = conn.execute(
        f"""
        UPDATE users
        SET {set_clause}
        WHERE username = ?
        """,
        values
    )
    conn.commit()
    if cursor.rowcount == 0:
        return {"message": f"No user found with username '{username}'."} 
       
    # # 只更新传入的字段
    # update_fields = {k: v for k, v in user.model_dump(exclude_unset=True).items() if v is not None}
    
    # if not update_fields:
    #     return {"message": "No fields to update."}

    # set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
    # values = list(update_fields.values())
    # values.append(username)  # 添加 username 到参数列表

    # cursor = conn.execute(
    #     f"""
    #     UPDATE users
    #     SET {set_clause}
    #     WHERE username = ?
    #     """,
    #     values
    # )
    # conn.commit()
    
    # if cursor.rowcount == 0:
    #     return {"message": f"No user found with username '{username}'."}
    
    # return {"message": f"User '{username}' updated.", "updated_fields": update_fields}

@app.delete("/user/{username}")
def delete_user(username: str, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.execute(
        """
        DELETE FROM users
        WHERE username = ?
        """,
        # (username)   # 字符串
        (username,)  # 只有一个元素的元组
    )
    conn.commit()
    if cursor.rowcount == 0:
        return {"message": f"No user found with username '{username}'."}
    return {"message": f"User '{username}' deleted."}