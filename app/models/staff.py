from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Enum as SQLAlchemyEnum
from app.core.database import Base
from sqlalchemy.orm import relationship



class Staff(Base):
    __tablename__ = "staff"

    id = Column(String, ForeignKey('users.id'), primary_key=True)
    staff_id = Column(String, index=True)
    branch_id = Column(String, ForeignKey('branches.id'))
    
    branches = relationship('Branch', back_populates='staff')