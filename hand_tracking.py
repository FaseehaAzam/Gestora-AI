
import cv2
import mediapipe as mp

# Initialize MediaPipe hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam")
    raise SystemExit

print("AIRCTRL Hand Tracking Started!")
print("Press Q to exit.")

while True:
    success, frame = cap.read()

    if not success:
        print("Cannot read camera frame")
        break

    # Mirror the webcam
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb_frame)

    # Draw 21 hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # Display webcam
    cv2.imshow("AIRCTRL - AI Hand Tracking", frame)

    # Press Q to close
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
