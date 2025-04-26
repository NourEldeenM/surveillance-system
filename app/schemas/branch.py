from typing import List
from pydantic import BaseModel

from schemas.user import UserResponse

class BranchCreate(BaseModel):  # Used for creating users
    address: str
    postal_code: str

class BranchResponse(BranchCreate):  # Used for returning users (includes ID)
    id: str
    address: str
    postal_code: str
    staff: List[UserResponse]