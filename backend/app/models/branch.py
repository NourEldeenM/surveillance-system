from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Branch(Base):
    __tablename__ = "branches"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid4()))
    region_id = Column(ForeignKey('regions.id'), index=True)
    branch_admin_id = Column(String, ForeignKey('branch_admins.id'), index=True)
    address = Column(String)
    postal_code = Column(String, index=True)
    
    region = relationship('Region', back_populates='branches')
    branch_admin = relationship('BranchAdmin', back_populates='branches')
    staff = relationship('Staff', back_populates='branches')
    # staff = relationship('Staff', 'branch') # should add in table class Staff attribute 