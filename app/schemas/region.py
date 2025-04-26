from typing import List
from pydantic import BaseModel
from models.region import RegionLocation
from schemas.branch import BranchResponse

class RegionCreate(BaseModel):
    region_location: RegionLocation
    
class RegionResponse(RegionCreate):
    id: str
    branches: List[BranchResponse]