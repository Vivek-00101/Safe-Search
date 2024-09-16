# 🕵️‍♂️ SAFE SEARCH: Finding Missing Person 

A real-time missing person detection system utilizing **InsightFace** for face recognition and an **IP Webcam** to capture live video feeds. The system allows users to submit missing person details, then monitors live surveillance footage, and sends notifications when a match is found.

## 🔧 Key Features

- **Face Recognition**: Leveraging the **InsightFace** library for real-time detection and recognition of missing persons.
- **Web-based Submission**: Families can submit missing person details and photos via a user-friendly web form.
- **Real-time Surveillance**: Integrates with **IP Webcam** to monitor live video feeds for face recognition.
- **Automated Notifications**: Sends SMS alerts to concerned parties with the exact location when a match is identified.
- **Data Management**: Organizes missing person data and recognized face images for future reference.

## 🚀 How to Run

1. Clone the repository:

    ```bash
    git clone https://github.com/Vivek-00101/Safe-Search.git
    cd safe-search
    ```

2. Install the required dependencies:

    ```bash
    pip install flask opencv-python-headless insightface numpy
    ```

3. Run the Flask app:

    ```bash
    python app.py
    ```

4. Open your browser and navigate to `http://localhost:5000` to use the system.

## 📷 IP Webcam Configuration

To configure your IP Webcam, update the stream URL in `camera.py`:

```python
self.video_capture = cv2.VideoCapture('rtsp://your_ip:your_port/your_stream.sdp')
