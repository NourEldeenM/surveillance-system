from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from schemas.user import UserCreate
from schemas.auth import TokenResponse, UserLogin
from services.user import UserService

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=TokenResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user and returns a JWT token."""
    return UserService.create_user(user_data, db)

@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """Logs in a user and returns a JWT token."""
    return UserService.authenticate_user(user_data.email, user_data.password, db)