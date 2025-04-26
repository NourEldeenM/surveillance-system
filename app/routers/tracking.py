from services.tracking import TrackingService
from core.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
import tempfile, os

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

@router.post("/video")
async def track_video(file: UploadFile = File(...)):
    """Endpoint to perform multi-object tracking on an uploaded video."""
    try:
        # Save uploaded video to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            data = await file.read()
            tmp.write(data)
            tmp.flush()
            video_path = tmp.name

        # Define output path
        output_path = video_path.replace(".mp4", "_annotated.mp4")
        # Process tracking (returns a dict)
        result = TrackingService.process_tracking(video_path, output_path)

        # Build response using dict keys
        return {
            "annotated_video": result.get("output"),
            "predictions": result.get("predictions")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))