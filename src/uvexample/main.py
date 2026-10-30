from fastapi import FastAPI
from pydantic import BaseModel,ConfigDict

class User(BaseModel):
    # 严格模式,检查模型属性，不开启的话，age：“18” 会转成18，
    model_config = ConfigDict(strict=True)
    username: str
    age: int
    full_name: str
    email: str

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
    user_dict = user.model_dump()
    users.append(user_dict) 
    return {"user": user_dict}

