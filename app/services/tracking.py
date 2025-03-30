import os
import logging
import cv2
import torch
from ultralytics import YOLO
import csv
import configparser
import numpy as np
import pandas as pd

from app.core.config import TRACKING
from app.core.redis import redis_client  # if you plan to cache tracking results
from app.utils.exceptions import DatabaseError, NotFoundError

logger = logging.getLogger(__name__)

class Tracker:
    def __init__(self, model_path='yolo12x.pt'):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model_path).to(self.device)
        with torch.amp.autocast(device_type=self.device, enabled=False):
            self.model.fuse()
        
        if self.device == 'cuda':
            self.model = self.model.half()
            print("Using FP16 precision on", self.device)
        else:
            print("Using FP32 precision on", self.device)

    def track_video(self, video_path, output_path='output.mp4'):
        """
        Process a video file by reading frame by frame,
        performing tracking, and writing the annotated video.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Could not open video file: {video_path}")
        
        # Get video metadata
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        imWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        imHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup VideoWriter using video metadata
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, frame_rate, (imWidth, imHeight))
        
        # Prepare predictions list and a file to save predictions
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        prediction_dir = os.path.join('tracker_results', 'data')
        os.makedirs(prediction_dir, exist_ok=True)
        prediction_file = os.path.join(prediction_dir, f'{video_name}.txt')
        predictions = []  # List to hold prediction rows
        frame_number = 1

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # End of video

            results = self.model.track(
                frame,
                persist=True,
                classes=0,
                conf=0.5,   # adjust as needed (e.g., 0.3, 0.4, 0.5)
                iou=0.55,   # adjust as needed (e.g., 0.45, 0.5, 0.55)
                verbose=False,
                device=self.device
            )
            
            # Annotate and write the processed frame to the output video.
            annotated_frame = results[0].plot()
            out.write(annotated_frame)

            # Collect predictions for each detected box with an assigned id.
            for box in results[0].boxes:
                if not hasattr(box, "id") or box.id is None:
                    continue
                tracked_id = int(box.id)
                bbox = box.xyxy.cpu().numpy()[0]
                x1, y1, x2, y2 = bbox.tolist()
                w = x2 - x1
                h = y2 - y1
                confidence = float(box.conf.cpu().numpy()[0])
                predictions.append([frame_number, tracked_id, x1, y1, w, h, confidence, -1, -1, -1])
            
            frame_number += 1

        cap.release()
        out.release()

        # Save predictions to a file
        with open(prediction_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(predictions)
        print(f"Predictions saved to {prediction_file}")
        return prediction_file


class TrackingService:
    @staticmethod
    def process_tracking(video_path: str, output_path: str):
        """
        Instantiate the tracker with the model and run the tracking process
        on the provided video file.
        """
        try:
            tracker = Tracker(model_path=TRACKING.TRACKING_MODEL_PATH)
            prediction_file = tracker.track_video(video_path, output_path)
            # Optionally, you can cache or record results in Redis here.
            return {"message": "Tracking completed", "output": output_path, "predictions": prediction_file}
        except Exception as e:
            logger.error(f"Error processing tracking: {e}")
            raise e
        # You can also implement caching logic here if needed.
    @staticmethod
    def get_tracking_results(video_path: str):
        """
        Retrieve tracking results from a video file.
        """
        try:
            # Check if the video file exists
            if not os.path.exists(video_path):
                raise NotFoundError(f"Video file not found: {video_path}")

            # Read the predictions from the CSV file
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            prediction_file = os.path.join('tracker_results', 'data', f'{video_name}.txt')
            if not os.path.exists(prediction_file):
                raise NotFoundError(f"Prediction file not found: {prediction_file}")

            df = pd.read_csv(prediction_file, header=None)
            df.columns = ['frame', 'id', 'x1', 'y1', 'w', 'h', 'confidence', 'class_id', 'class_name', 'timestamp']
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error retrieving tracking results: {e}")
            raise e
    @staticmethod
    def get_tracking_statistics(video_path: str):
        """
        Calculate and return statistics from the tracking results.
        """
        try:
            # Retrieve tracking results
            results = TrackingService.get_tracking_results(video_path)
            if not results:
                raise NotFoundError("No tracking results found.")

            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(results)

            # Calculate statistics
            total_frames = df['frame'].nunique()
            total_objects = df['id'].nunique()
            avg_confidence = df['confidence'].mean()

            return {
                "total_frames": total_frames,
                "total_objects": total_objects,
                "avg_confidence": avg_confidence
            }
        except Exception as e:
            logger.error(f"Error calculating tracking statistics: {e}")
            raise e
    @staticmethod
    def save_tracking_results_to_csv(video_path: str, output_csv_path: str):
        """
        Save tracking results to a CSV file.
        """
        try:
            # Retrieve tracking results
            results = TrackingService.get_tracking_results(video_path)
            if not results:
                raise NotFoundError("No tracking results found.")

            # Convert to DataFrame and save as CSV
            df = pd.DataFrame(results)
            df.to_csv(output_csv_path, index=False)
            return {"message": "Tracking results saved to CSV", "output": output_csv_path}
        except Exception as e:
            logger.error(f"Error saving tracking results to CSV: {e}")
            raise e
    @staticmethod
    def cache_tracking_results(video_path: str):
        """
        Cache tracking results in Redis.
        """
        try:
            # Retrieve tracking results
            results = TrackingService.get_tracking_results(video_path)
            if not results:
                raise NotFoundError("No tracking results found.")

            # Cache the results in Redis
            redis_key = f"tracking:{os.path.basename(video_path)}"
            redis_client.set(redis_key, str(results))
            return {"message": "Tracking results cached", "redis_key": redis_key}
        except Exception as e:
            logger.error(f"Error caching tracking results: {e}")
            raise e
    @staticmethod
    def retrieve_cached_tracking_results(redis_key: str):
        """
        Retrieve cached tracking results from Redis.
        """
        try:
            # Retrieve the cached results from Redis
            cached_results = redis_client.get(redis_key)
            if not cached_results:
                raise NotFoundError("No cached tracking results found.")
            return eval(cached_results)  # Convert string back to list of dicts
        except Exception as e:
            logger.error(f"Error retrieving cached tracking results: {e}")
            raise e
    @staticmethod
    def delete_cached_tracking_results(redis_key: str):
        """
        Delete cached tracking results from Redis.
        """
        try:
            # Delete the cached results from Redis
            redis_client.delete(redis_key)
            return {"message": "Cached tracking results deleted"}
        except Exception as e:
            logger.error(f"Error deleting cached tracking results: {e}")
            raise e
    @staticmethod
    def get_tracking_results_from_redis(redis_key: str):
        """
        Retrieve tracking results from Redis.
        """
        try:
            # Check if the tracking results are cached in Redis
            cached_results = redis_client.get(redis_key)
            if not cached_results:
                raise NotFoundError("No cached tracking results found.")
            return eval(cached_results)  # Convert string back to list of dicts
        except Exception as e:
            logger.error(f"Error retrieving tracking results from Redis: {e}")
            raise e
    @staticmethod
    def clear_tracking_cache():
        """
        Clear all cached tracking results from Redis.
        """
        try:
            # Clear all cached tracking results
            redis_client.flushdb()
            return {"message": "All cached tracking results cleared"}
        except Exception as e:
            logger.error(f"Error clearing tracking cache: {e}")
            raise e
    @staticmethod
    def get_tracking_model_info():
        """
        Get information about the tracking model.
        """
        try:
            # Load the model configuration
            config = configparser.ConfigParser()
            config.read(TRACKING.TRACKING_MODEL_CONFIG)
            model_info = {
                "model_path": TRACKING.TRACKING_MODEL_PATH,
                "input_size": TRACKING.INPUT_SIZE,
                "confidence_threshold": TRACKING.CONFIDENCE_THRESHOLD,
                "nms_threshold": TRACKING.NMS_THRESHOLD
            }
            return model_info
        except Exception as e:
            logger.error(f"Error retrieving tracking model info: {e}")
            raise e
    @staticmethod
    def validate_tracking_model():
        """
        Validate the tracking model by checking its existence and loading it.
        """
        try:
            if not os.path.exists(TRACKING.TRACKING_MODEL_PATH):
                raise FileNotFoundError(f"Tracking model not found: {TRACKING.TRACKING_MODEL_PATH}")
            # Load the model to ensure it's valid
            Tracker(model_path=TRACKING.TRACKING_MODEL_PATH)
            return {"message": "Tracking model is valid"}
        except Exception as e:
            logger.error(f"Error validating tracking model: {e}")
            raise e
    @staticmethod
    def get_tracking_model_performance():
        """
        Get performance metrics of the tracking model.
        """
        try:
            # Load the model and get performance metrics
            model = Tracker(model_path=TRACKING.TRACKING_MODEL_PATH)
            performance_metrics = {
                "model_path": TRACKING.TRACKING_MODEL_PATH,
                "input_size": TRACKING.INPUT_SIZE,
                "confidence_threshold": TRACKING.CONFIDENCE_THRESHOLD,
                "nms_threshold": TRACKING.NMS_THRESHOLD
            }
            return performance_metrics
        except Exception as e:
            logger.error(f"Error retrieving tracking model performance: {e}")
            raise e