README for Hand Gesture Recognition with Speech Feedback
=======================================================

Overview
--------
This Python script captures live video from your webcam, detects a single hand using MediaPipe, recognizes a set of predefined hand‐gestures, and optionally speaks the name of each gesture aloud via text‐to‐speech.

Supported Gestures
------------------
- **Thumbs Up**  
- **Open Palm**  
- **Fist**  
- **Peace** (index & middle fingers extended)  
- **Okay** (thumb & index pinch + other fingers extended)  
- **Pointing** (index finger extended only)  
- **Rock** (index & pinky extended)  
- **Call Me** (thumb & pinky extended)  

Any unrecognized combination will be labeled “Unknown Gesture.” When no hand is visible, it displays “No Hand Detected.”

Requirements
------------
- Python 3.7 or newer  
- OpenCV (`cv2`)  
- MediaPipe (`mediapipe`)  
- pyttsx3 (offline text‐to‐speech)  
- A working webcam  

Installation
------------
1. **Clone or download** this repository to your local machine.  
2. **Create and activate** a Python virtual environment (recommended):  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
