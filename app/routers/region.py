from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from schemas.region import RegionCreate, RegionResponse
from services.region import RegionService

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=RegionResponse)
def create_region_route(region_data: RegionCreate, db: Session = Depends(get_db)):
    return RegionService.create_region(region_data, db)

@router.get("", response_model=List[RegionResponse])
def get_all_regions_route(db: Session = Depends(get_db)):
    return RegionService.get_all_regions(db)

@router.get("/{id}", response_model=RegionResponse)
def get_region_by_id_route(id: str, db: Session = Depends(get_db)):
    return RegionService.get_region_by_id(id, db)

@router.patch("/{id}", response_model=RegionResponse)
def update_region_by_id_route(id: str, region_data: RegionCreate, db: Session = Depends(get_db)):
    return RegionService.update_region_by_id(id, region_data, db)