from fastapi import APIRouter, HTTPException, Depends
from app.services.tracking import TrackingService
from app.core.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def track_objects(sequence_path: str, output_path: str = "output.mp4"):
    """
    Endpoint to perform multi-object tracking on a given sequence.
    """
    try:
        result = TrackingService.process_tracking(sequence_path, output_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))