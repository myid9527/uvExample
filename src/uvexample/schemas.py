from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str | None = None
    age: int
    full_name: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    # 它告诉 Pydantic：
# 不要只从字典读取数据，也允许从对象属性读取数据
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    age: int
    full_name: str
    email: EmailStr

class UserUpdate(BaseModel):
    username: str | None = None
    age: int | None = None
    full_name: str | None = None
    email: str | None = None