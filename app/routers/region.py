from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.schemas.region import RegionCreate, RegionResponse
from app.services.region import RegionService

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=RegionResponse)
def create_branch_route(region_data: RegionCreate, db: Session = Depends(get_db)):
    return RegionService.create_region(region_data, db)