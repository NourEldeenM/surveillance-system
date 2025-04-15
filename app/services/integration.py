import os
import cv2
import pandas as pd
import tempfile
import logging

from app.services.tracking import TrackingService
from app.services.face import FaceService  # adjust import based on your project structure

logger = logging.getLogger(__name__)

class IntegrationService:
    @staticmethod
    def process_video_integration(video_path: str, output_path: str):
        """
        Process a video by first performing tracking, and then for each detected bounding box,
        crop the region from the frame and perform face recognition.
        Returns integrated results per frame.
        """
        # Run tracking on the video; this creates an annotated output video and a CSV file with predictions.
        tracking_result = TrackingService.process_tracking(video_path, output_path)
        predictions_file = tracking_result.get("predictions")
        if not predictions_file or not os.path.exists(predictions_file):
            raise ValueError("Tracking predictions file not found.")

        # Read the tracking predictions into a DataFrame.
        df = pd.read_csv(predictions_file, header=None)
        # Set column names so that we know what each field is.
        df.columns = ['frame', 'id', 'x1', 'y1', 'w', 'h', 'confidence', 'class_id', 'class_name', 'timestamp']

        # Open the video to extract frames for face cropping.
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Unable to open video file: {video_path}")

        integrated_results = []
        frame_number = 1

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # End of video reached

            # Filter predictions for the current frame.
            preds = df[df['frame'] == frame_number]
            faces_info = []

            # Process every detection in this frame.
            for _, row in preds.iterrows():
                # Get bounding box coordinates; note that tracking returns [x1, y1, w, h]
                x1 = int(row['x1'])
                y1 = int(row['y1'])
                w = int(row['w'])
                h = int(row['h'])

                # Ensure coordinates are within the frame boundaries.
                x2 = min(x1 + w, frame.shape[1])
                y2 = min(y1 + h, frame.shape[0])
                if x1 < 0 or y1 < 0 or x2 <= x1 or y2 <= y1:
                    continue

                # Crop the face region.
                face_crop = frame[y1:y2, x1:x2]

                # Write the cropped face to a temporary file.
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_face:
                    temp_face_path = temp_face.name
                    cv2.imwrite(temp_face_path, face_crop)

                # Run face recognition on the cropped image.
                face_label = FaceService.recognize_face(temp_face_path)
                os.remove(temp_face_path)  # Clean up the temporary file.

                faces_info.append({
                    "tracked_id": int(row['id']),
                    "bbox": [x1, y1, w, h],
                    "confidence": float(row['confidence']),
                    "face_recognition": face_label
                })

            if faces_info:
                integrated_results.append({
                    "frame": frame_number,
                    "faces": faces_info
                })

            frame_number += 1

        cap.release()
        return integrated_results