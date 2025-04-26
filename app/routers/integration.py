import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.integration import IntegrationService

router = APIRouter()

@router.post("/video")
async def integrate_models(video: UploadFile = File(...)):
    """
    Endpoint to run both tracking and face recognition on an uploaded video.
    Returns per-frame integrated results (e.g., tracked face IDs with recognition labels).
    """
    try:
        # Save the uploaded video to a temporary file.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            contents = await video.read()
            temp_video.write(contents)
            temp_video_path = temp_video.name

        # Define output video path (this could be a temporary file or a defined directory).
        output_video_path = temp_video_path.replace(".mp4", "_output.mp4")

        # Run the integration processing.
        results = IntegrationService.process_video_integration(temp_video_path, output_video_path)

        # Optionally, you might want to include the paths of generated video/prediction files.
        return {
            "message": "Integration completed successfully.",
            "results": results,
            "annotated_video": output_video_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
