from uuid import uuid4
from sqlalchemy.orm import Session
from app.schemas.branch import BranchCreate, BranchResponse
from app.models.branch import Branch
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.utils.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class BranchService:
    @staticmethod
    def create_branch(branch_data: BranchCreate, db: Session) -> BranchResponse:
        """Creates a new branch."""
        try:
            branch = Branch(
                id=str(uuid4()),
                address=branch_data.address,
                postal_code=branch_data.postal_code,
                staff=[]
            )
            db.add(branch)
            db.commit()
            db.refresh(branch)
            return branch
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while creating user: {e}")
            raise DatabaseError(detail="A database error occurred while creating the user.")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error while creating user: {e}")
            raise DatabaseError(detail="An unexpected error occurred while creating the user.")