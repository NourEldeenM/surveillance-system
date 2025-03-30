from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VisitorLogCreate(BaseModel):
    visitor_id: str
    branch_id: Optional[str] = None  # if branch-specific logging is desired

class VisitorLogResponse(VisitorLogCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class AttendanceCreate(BaseModel):
    employee_id: str
    check_in: datetime
    check_out: Optional[datetime] = None

class AttendanceResponse(AttendanceCreate):
    id: int

    class Config:
        orm_mode = True