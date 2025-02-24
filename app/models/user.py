from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum, ARRAY
from app.database import Base

class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    super_user = "super_user"
    admin = "admin"
    staff = "staff"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    gender = Column(SQLAlchemyEnum(Gender), nullable=False)
    roles = Column(ARRAY(SQLAlchemyEnum(Role)), nullable=False)
