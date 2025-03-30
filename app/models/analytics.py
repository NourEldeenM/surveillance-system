from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class VisitorLog(Base):
    __tablename__ = "visitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    visitor_id = Column(String, index=True)  # e.g., IP address or a unique session identifier
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True)  # Optional: if you want to track branch-specific visits
    visit_duration = Column(Integer, nullable=True)  # Optional: to store visit duration in seconds

    # Optional: set up a relationship to a branch if needed
    branch = relationship("Branch", back_populates="visitor_logs")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("users.id"), nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=False)
    status = Column(String, default="present")  # e.g., present, absent, leave, etc.
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Optional: set up a relationship to the employee (user) model if needed
    employee = relationship("User", back_populates="attendances")
