from fastapi import APIRouter, UploadFile, File
import tempfile
from app.core.database import SessionLocal
from app.services.face import FaceService

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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name
        
    result = FaceService.recognize_face(temp_path)
    return result
