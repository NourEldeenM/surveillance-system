from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Enum as SQLAlchemyEnum
from core.database import Base
from sqlalchemy.orm import relationship



class BranchAdmin(Base):
    __tablename__ = "branch_admins"

    id = Column(String, ForeignKey('users.id'), primary_key=True)
    branch_admin_id = Column(String, index=True)
    
    branches = relationship('Branch', back_populates='branch_admin')