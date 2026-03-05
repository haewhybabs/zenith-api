from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# What the user sends us when signing up
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# What we send back to the user when they sign up or log in
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)