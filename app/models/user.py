from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum
from core.database import Base
from sqlalchemy.orm import relationship

class Gender(str, Enum):
    male = "MALE"
    female = "FEMALE"

class Role(str, Enum):
    super_user = "SUPER_USER"
    admin = "ADMIN"
    branch_admin = "BRANCH_ADMIN"
    staff = "STAFF"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False) # hashed
    gender = Column(SQLAlchemyEnum(Gender), nullable=False)
    role = Column(SQLAlchemyEnum(Role), nullable=False)
    profile_picture = Column(String)

    attendances = relationship("Attendance", back_populates="employee")