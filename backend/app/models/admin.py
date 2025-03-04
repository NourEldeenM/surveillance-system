from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Enum as SQLAlchemyEnum
from app.core.database import Base
from sqlalchemy.orm import relationship



class Admin(Base):
    __tablename__ = "admins"

    id = Column(String, ForeignKey('users.id'), primary_key=True)
    admin_id = Column(String, index=True)
    
    regions = relationship('Region', back_populates='admin')