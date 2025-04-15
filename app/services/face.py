import pickle
import numpy as np
from deepface import DeepFace

# Load saved embeddings
with open("./assets/embeddings.pkl", "rb") as f:
    known_embeddings = pickle.load(f)
    
print(type(known_embeddings))
print(len(known_embeddings))  # Number of elements in the list
# print(known_embeddings[0])  # Print first two items to inspect

# Extract metadata
model_name = known_embeddings["model_name"]
threshold = known_embeddings["threshold"]
embeddings_dict = known_embeddings["embeddings_dict"]


class FaceService:
    @staticmethod
    def recognize_face(image_path, threshold=0.5):
        try:
            embedding_obj = DeepFace.represent(image_path, model_name=model_name, detector_backend="yolov8")[0]["embedding"]
        except Exception as e:
            print(f"Error: {e}")
            return "doesn't_exist"

        best_match = None
        best_similarity = -1

        embeddings_dict = known_embeddings["embeddings_dict"]
        
        for person, known_embedding_list in embeddings_dict.items():
            mean_known_embedding = np.mean(known_embedding_list, axis=0)

            similarity = np.dot(embedding_obj, mean_known_embedding) / (np.linalg.norm(embedding_obj) * np.linalg.norm(mean_known_embedding))

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = person

        return best_match if best_similarity >= threshold else "doesn't_exist"