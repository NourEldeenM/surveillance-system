from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import user
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy.exc import IntegrityError

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserResponse)  # Response uses Pydantic model
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = user.User(
            id=str(uuid4()),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            gender=user_data.gender,
            roles=user_data.roles
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()  # Rollback the transaction to keep DB consistent
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        db.rollback()  # Ensure rollback for any unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred:\n{e}")
    
@app.get("/users/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(user.User).all()  # Returns list of UserResponse
