import cv2
from models.face_recognition_model import FaceRecognitionModel
from models.file_manager import FileManager

class Camera:
    def __init__(self):
        self.video_capture = cv2.VideoCapture('rtsp://192.0.0.4:8081/h264_pcm.sdp')
        self.recognition_model = FaceRecognitionModel()
        self.file_manager = FileManager()

    def start_detection(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret or frame is None:
                print("Error: Unable to capture frame from camera.")
                break
            
            # Get the frame dimensions
            frame_height, frame_width = frame.shape[:2]

            # Detect faces
            faces, names = self.recognition_model.recognise_faces(frame)

            for (x, y, w, h), name in zip(faces, names):
                if name and name != "Unknown":
                    # Ensure the region of interest (ROI) is valid and within bounds
                    if 0 <= x < frame_width and 0 <= y < frame_height and w > 0 and h > 0:
                        if x + w <= frame_width and y + h <= frame_height:
                            cropped_frame = frame[y:y+h, x:x+w]
                            if cropped_frame.size != 0:
                                self.file_manager.save_recognised_person(name, cropped_frame)
                            else:
                                print(f"Warning: Cropped frame is empty for detected face: {name}")
                        else:
                            print(f"Warning: Cropped area exceeds frame bounds for {name} at (x={x}, y={y}, w={w}, h={h})")
                    else:
                        print(f"Warning: Invalid or out-of-bounds face region for {name} at (x={x}, y={y}, w={w}, h={h})")
            
            # Display the resulting frame
            #cv2.imshow('Video', frame)
            print("Processing frame...")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.video_capture.release()
        cv2.destroyAllWindows()
