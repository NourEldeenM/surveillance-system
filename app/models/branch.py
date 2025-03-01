from typing import List
from uuid import uuid4
from sqlalchemy import Column, String
from app.models.database import Base
from app.models.user import User
from sqlalchemy.orm import relationship, Mapped

class Branch(Base):
    __tablename__ = "branches"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    address = Column(String, index=True)
    postal_code = Column(String, index=True)
    staff: Mapped[List["User"]] = relationship(back_populates="branch")