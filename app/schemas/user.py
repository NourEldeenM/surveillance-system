from os import strerror
from pydantic import BaseModel, EmailStr
from app.models.user import Gender, Role

class UserCreate(BaseModel):  # Used for creating users
    first_name: str
    last_name: str
    email: EmailStr
    password: str # plain
    gender: Gender
    role: Role
    profile_picture: str
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_enums

    @classmethod
    def validate_enums(cls, values):
        values["gender"] = values["gender"].lower()
        values["role"] = values["role"].lower()
        return values

class UserResponse(UserCreate):  # Used for returning users (includes ID)
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    gender: Gender
    role: Role
    profile_picture: str