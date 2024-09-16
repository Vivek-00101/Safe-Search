import os
import cv2
import numpy as np
import pickle
from insightface.app import FaceAnalysis

class FaceRecognitionModel:
    def __init__(self):
        self.face_app = FaceAnalysis(providers=['CUDAExecutionProvider'])
        self.face_app.prepare(ctx_id=0, det_size=(640, 640))
        self.known_faces = self.load_known_faces()
        self.recognition_threshold = 0.9  # Set threshold for recognition

    def load_known_faces(self):
        # Load known faces from the 'missing' folder and save them in the `known_faces` dictionary
        known_faces = {}
        for file in os.listdir("static/missing/"):
            if file.endswith(".jpg"):
                name = file.split(".")[0]
                img = cv2.imread(os.path.join("static/missing/", file))
                faces = self.face_app.get(img)
                if faces:
                    known_faces[name] = faces[0].normed_embedding
        return known_faces

    def recognise_faces(self, frame):
        # Recognize faces in the provided frame
        faces = self.face_app.get(frame)
        names = []
        for face in faces:
            face_embedding = face.normed_embedding
            best_match = self.identify_face(face_embedding)
            names.append(best_match)
        return [(int(face.bbox[0]), int(face.bbox[1]), int(face.bbox[2]-face.bbox[0]), int(face.bbox[3]-face.bbox[1])) for face in faces], names

    def identify_face(self, face_embedding):
        min_distance = float('inf')
        best_match_label = "Unknown"
        for label, known_embedding in self.known_faces.items():
            distance = np.linalg.norm(known_embedding - face_embedding)
            if distance < min_distance:
                min_distance = distance
                best_match_label = label
        if min_distance <= self.recognition_threshold:
            return best_match_label
        else:
            return "Unknown"
