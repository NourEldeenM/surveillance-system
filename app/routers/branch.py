from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from schemas.branch import BranchCreate, BranchResponse
from services.branch import BranchService

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=BranchResponse)
def create_branch_route(branch_data: BranchCreate, db: Session = Depends(get_db)):
    return BranchService.create_branch(branch_data, db)