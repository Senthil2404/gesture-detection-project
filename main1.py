import cv2
import mediapipe as mp
import pyttsx3
import time

# Initialize MediaPipe Hands and Drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Helper function to check if a finger is open (tip above PIP joint)
def finger_is_open(landmarks, tip, pip):
    return landmarks[tip].y < landmarks[pip].y

# Calculate Euclidean distance between two landmarks
def distance(a, b):
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Set up webcam
cap = cv2.VideoCapture(0)

last_gesture = None
last_speak_time = 0
speak_interval = 2  # seconds between speech to avoid overlap

# Configure the Hands model
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty frame.")
            continue

        # Flip the image horizontally for natural viewing
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        gesture = "No Hand Detected"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark

                # Check each finger state
                thumb_open = finger_is_open(landmarks, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP)
                index_open = finger_is_open(landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP)
                middle_open = finger_is_open(landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP)
                ring_open = finger_is_open(landmarks, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP)
                pinky_open = finger_is_open(landmarks, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)

                thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Define gestures
                if thumb_open and not index_open and not middle_open and not ring_open and not pinky_open:
                    gesture = "Thumbs Up"
                elif all([thumb_open, index_open, middle_open, ring_open, pinky_open]):
                    gesture = "Open Palm"
                elif not any([thumb_open, index_open, middle_open, ring_open, pinky_open]):
                    gesture = "Fist"
                elif index_open and middle_open and not ring_open and not pinky_open:
                    gesture = "Peace"
                elif distance(thumb_tip, index_tip) < 0.05 and middle_open and ring_open and pinky_open:
                    gesture = "Okay"
                elif index_open and not any([middle_open, ring_open, pinky_open]):
                    gesture = "Pointing"
                elif index_open and pinky_open and not middle_open and not ring_open:
                    gesture = "Rock"
                elif thumb_open and pinky_open and not index_open and not middle_open and not ring_open:
                    gesture = "Call Me"
                else:
                    gesture = "Unknown Gesture"

        # Show gesture on screen
        cv2.putText(image, f'Gesture: {gesture}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Speak gesture if changed and cooldown time passed
        current_time = time.time()
        if gesture != last_gesture and current_time - last_speak_time > speak_interval:
            if gesture != "No Hand Detected" and gesture != "Unknown Gesture":
                speak(gesture)
                last_speak_time = current_time
                last_gesture = gesture

        cv2.imshow('Gesture Recognition', image)

        if cv2.waitKey(5) & 0xFF == 27:  # ESC key to quit
            break

cap.release()
cv2.destroyAllWindows()
