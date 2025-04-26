from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.security import Security
from models import user
from schemas.user import UserCreate, UserResponse
from typing import List
import logging
from utils.exceptions import DuplicateEmailError, DatabaseError, NotFoundError, UnauthorizedError

# Set up logging
logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def create_user(user_data: UserCreate, db: Session) -> UserResponse:
        """Creates a new user"""
        try:
            hashed_password = Security.hash_password(user_data.password)
            new_user = user.User(
                id=str(uuid4()),
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email,
                password=hashed_password,
                gender=user_data.gender,
                role=user_data.role
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except IntegrityError as e:
            db.rollback()
            logger.error(f"IntegrityError while creating user: {e}")
            if "duplicate key value violates unique constraint" in str(e):
                raise DuplicateEmailError(email=user_data.email)
            else:
                raise DatabaseError(detail="A database integrity error occurred.")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while creating user: {e}")
            raise DatabaseError(detail="A database error occurred while creating the user.")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error while creating user: {e}")
            raise DatabaseError(detail="An unexpected error occurred while creating the user.")

    @staticmethod
    def get_users(db: Session) -> List[UserResponse]:
        """Gets all users in the database"""
        try:
            return db.query(user.User).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching users: {e}")
            raise DatabaseError(detail="A database error occurred while fetching users.")
        except Exception as e:
            logger.error(f"Unexpected error while fetching users: {e}")
            raise DatabaseError(detail="An unexpected error occurred while fetching users.")

    @staticmethod
    def get_user_by_id(user_id: str, db: Session) -> UserResponse:
        """Gets a user by id"""
        query_user = db.query(user.User).filter(user.User.id == user_id).first()
        if not query_user:
            raise NotFoundError(resource="User", identifier=user_id)
        return query_user
    
    @staticmethod
    def update_user_by_id(user_id: str, user_data: UserCreate ,db: Session) -> UserResponse:
        """Updates an existing user partially."""
        query_user = db.query(user.User).filter(user.User.id == user_id).first()

        if not query_user:
            raise NotFoundError(resource="User", identifier=user_id)

        # Update only the provided fields
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(query_user, key, value)

        db.commit()
        db.refresh(query_user)
        return query_user
    
    @staticmethod
    def authenticate_user(email: str, password: str, db: Session):
        """Authenticates user and returns access token."""
        query_user = db.query(user.User).filter(user.User.email == email).first()
        if not query_user or not Security.verify_password(password, query_user.password):
            raise UnauthorizedError("Invalid email or password")

        access_token = Security.create_access_token(UserService.convert_user_to_dict(query_user))
        return {"access_token": access_token, "token_type": "bearer"}
    
    @staticmethod
    def delete_user(id: str, db: Session):
        query_user = UserService.get_user_by_id(id, db)
        db.delete(query_user)
        db.commit()
        return {"message": f"User with ID {id} has been deleted"}
    
    @staticmethod
    def convert_user_to_dict(user: user.User):
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "gender": user.gender,
            "role": user.role
        }