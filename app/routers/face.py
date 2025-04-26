from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
from core.database import SessionLocal
from services.face import FaceService

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    """Endpoint to recognize a face from an uploaded image"""
    try:
        # Save temp image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        result = FaceService.recognize_face(temp_path)
        return {"label": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
