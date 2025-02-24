from pydantic import BaseModel, EmailStr
from typing import List
from app.models.user import Gender, Role

class UserCreate(BaseModel):  # Used for creating users
    first_name: str
    last_name: str
    email: EmailStr
    gender: Gender
    roles: List[Role]

class UserResponse(UserCreate):  # Used for returning users (includes ID)
    id: str

    class Config:
        from_attributes = True  # Converts ORM object to Pydantic model
