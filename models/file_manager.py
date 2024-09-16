import os
import json
import cv2  

class FileManager:
    def __init__(self):
        self.missing_dir = "static/missing/"
        self.recognised_dir = "static/recognised/"

    def save_missing_person(self, name, phone, photo):
        # Create a folder if it doesn't exist
        if not os.path.exists(self.missing_dir):
            os.makedirs(self.missing_dir)
        
        # Save photo
        photo_path = os.path.join(self.missing_dir, f"{name}.jpg")
        photo.save(photo_path)
        
        # Create JSON file with details
        details = {"name": name, "phone": phone, "photo_path": photo_path}
        with open(os.path.join(self.missing_dir, f"{name}.json"), 'w') as json_file:
            json.dump(details, json_file)

    def save_recognised_person(self, name, frame):
        # Create folder if it doesn't exist
        person_folder = os.path.join(self.recognised_dir, name)
        if not os.path.exists(person_folder):
            os.makedirs(person_folder)
        
        # Save frame
        frame_path = os.path.join(person_folder, f"{name}_{len(os.listdir(person_folder))}.jpg")
        cv2.imwrite(frame_path, frame)
