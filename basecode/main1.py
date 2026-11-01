from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,ConfigDict

class User(BaseModel):
    # 严格模式,检查模型属性，不开启的话，age：“18” 会转成18，
    model_config = ConfigDict(strict=True)
    # None = None 也就是可选类型，默认值为None,如果不设置默认值，代表参数还是必选，只不过可以接受None
    username: str | None = None
    age: int | None = None
    full_name: str | None = None
    email: str | None = None

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}



status = "healthy"

users = [
    {"id": 1, "username": "johndoe", "age": 30, "full_name": "<NAME>", "email": ""},
    {"id": 2, "username": "alice", "age": 25, "full_name": "Alice", "email": ""},
]


@app.get("/health")
def read_health():
    return {"status": status}
    
@app.get("/user")
def read_user(user_id: int | None = None):
    user = next((user for user in users if user["id"] == user_id), None)
    # return {"user_id": user_id, "user": user} if user else {"user_id": user_id, "user": None}
    if user_id:
        return {"user_id": user_id, "user": user} if user else {"user_id": user_id, "user": None}
    else:
        return users

@app.post("/user")
def create_user(user: User):
    # user_dict = user.dict()    # pydantic版本为v1
    # pydantic版本为v2，使用model_dump()方法将模型转换为字典
    # user_dict = user.model_dump()


    # 理解 exclude_unset=True
    # 它的作用是：只导出创建模型时明确传入的字段，排除未设置的字段。
    # 这在 PATCH 更新接口中非常有用。
    user_dict = user.model_dump(exclude_unset=True)
    users.append(user_dict) 
    return {"user": user_dict}

@app.patch("/user/{user_id}")
def update_user(user_id: int, user: User):
    existing_user = next((u for u in users if u["id"] == user_id), None)
    if existing_user:
        # 使用 exclude_unset=True 只更新传入的字段
        update_data = user.model_dump(exclude_unset=True)
        existing_user.update(update_data)
        return {"user_id": user_id, "user": existing_user}
    # 3. raise 和 return 有什么区别？
    # 这是重点。
    # 	     return	     raise
    # 作用	正常返回结果	抛出异常
    # 是否结束当前函数	是	中断正常流程
    # FastAPI 默认状态码	200	由 HTTPException 指定
    # 典型场景	查询成功	用户不存在、权限不足等
    raise HTTPException(status_code=404, detail="用户不存在")