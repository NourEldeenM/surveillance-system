import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.integration import IntegrationService
from services.tracking import TrackingService
import shutil

router = APIRouter()

@router.post("/video")
async def integrate_models(file: UploadFile = File(...)):
    # save upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(await file.read())
        tmp.flush()
        input_path = tmp.name

    # define a temp output path (will be copied by TrackingService)
    annotated_temp = input_path.replace(".mp4", "_annotated.mp4")

    # 1) Run tracking & get URL + predictions-file
    tracking_result = TrackingService.process_tracking(input_path, annotated_temp)
    http_url = tracking_result["output"]
    predictions_file = tracking_result["predictions"]

    # 2) Load predictions & do face cropping as before
    integrated = IntegrationService.process_video_integration(input_path, annotated_temp)


    return {
        "message": "Integration completed successfully.",
        "annotated_video": http_url, 
        "results": integrated
        }
