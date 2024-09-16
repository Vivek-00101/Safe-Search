from flask import Flask, render_template, request, redirect, url_for, session
from models.file_manager import FileManager
from models.camera import Camera
from models.face_recognition_model import FaceRecognitionModel
import threading


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Dummy user data for demo purposes
users = {'admin': 'password'}  # Replace with a database for production

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/details')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Debug: Print login attempt
        print(f"Login attempt: Username={username}, Password={password}")
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/details')
        return "Invalid credentials, please try again."
    
    return render_template('login.html')

@app.route('/details', methods=['GET', 'POST'])
def details():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        photo = request.files['photo']

        # Debug: Print form data
        print(f"Received details: Name={name}, Phone={phone}")

        # Save details using FileManager
        file_manager = FileManager()
        file_manager.save_missing_person(name, phone, photo)
        return redirect('/details')
    
    # Debug: Confirm rendering form
    print("Rendering form...")
    return render_template('form.html')

@app.route('/find')
def find():
    if 'username' not in session:
        return redirect('/login')

    # Start real-time face recognition in a background thread
    def start_camera_in_background():
        camera = Camera()
        camera.start_detection()  # This starts the detection process

    detection_thread = threading.Thread(target=start_camera_in_background)
    detection_thread.start()

    # Return the message immediately after starting the detection in the background
    return "Camera is active for finding the missing person. You will be notified after recognition."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
