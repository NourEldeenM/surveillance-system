from uuid import uuid4
from sqlalchemy.orm import Session
from schemas.region import RegionCreate, RegionResponse
from models.region import RegionLocation,  Region
from uuid import uuid4
from sqlalchemy.orm import Session
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from utils.exceptions import DatabaseError, NotFoundError

logger = logging.getLogger(__name__)


class RegionService:
    @staticmethod
    def create_region(region_data: RegionCreate, db: Session) -> RegionResponse:
        """Creates a new region."""
        try:
            location = RegionLocation(region_data.region_location.full_name, region_data.region_location.iso_code)
            region = Region(
                id=str(uuid4()),
                region_location=location.model_dump(),
            )
            db.add(region)
            db.commit()
            db.refresh(region)
            return region
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while creating region: {e}")
            raise DatabaseError(detail="A database error occurred while creating the region.")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error while creating region: {e}")
            raise DatabaseError(detail="An unexpected error occurred while creating the region.")
   
    @staticmethod     
    def get_all_regions(db: Session):
        """Gets all regions in the database"""
        try:
            return db.query(Region).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching regions: {e}")
            raise DatabaseError(detail="A database error occurred while fetching regions.")
        except Exception as e:
            logger.error(f"Unexpected error while fetching regions: {e}")
            raise DatabaseError(detail="An unexpected error occurred while fetching regions.")
        
    @staticmethod
    def get_region_by_id(region_id: str, db: Session):
        """Retrieves a region and converts JSON to a Pydantic model."""
        region = db.query(Region).filter(Region.id == region_id).first()
        if not region:
            return NotFoundError("Region", region_id)

        # convert json back to pydantic model
        region.region_location = RegionLocation(**region.region_location)
        return region
    
    @staticmethod
    def update_region_by_id(region_id: str, region_data: RegionCreate ,db: Session) -> RegionResponse:
        """Updates an existing region partially."""
        query_region = db.query(Region).filter(Region.id == region_id).first()

        if not query_region:
            raise NotFoundError(resource="Region", identifier=region_id)

        # Update only the provided fields
        for key, value in region_data.model_dump(exclude_unset=True).items():
            setattr(query_region, key, value)

        db.commit()
        db.refresh(query_region)
        return query_region