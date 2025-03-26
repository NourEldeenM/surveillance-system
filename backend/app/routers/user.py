from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from backend.app.schemas.utils import MessageResponse

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=UserResponse)
def create_user_route(user_data: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(user_data, db)

@router.get("", response_model=list[UserResponse])
def get_users_route(db: Session = Depends(get_db)):
    return UserService.get_users(db)

@router.get("/{id}", response_model=UserResponse)
def get_single_user_route(id: str, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(id, db)

@router.patch("/{id}", response_model=UserResponse)
def update_user_route(id: str, user_data: UserCreate ,db: Session = Depends(get_db)):
    return UserService.update_user_by_id(id, user_data ,db)

@router.delete("/{id}", response_model=MessageResponse)
def delete_user_route(id: str, db: Session = Depends(get_db)):
    return UserService.delete_user(id, db)