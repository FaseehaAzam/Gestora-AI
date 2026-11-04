


import cv2
import mediapipe as mp
import pyautogui
import time
import math

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam not found!")
    raise SystemExit

# Cursor smoothing
previous_x, previous_y = pyautogui.position()
smoothing = 0.25

# Click settings
click_threshold = 0.04
pinch_released = True
last_click_time = 0
click_cooldown = 0.5

print("AIRCTRL Virtual Mouse Started!")
print("Move index finger = Move cursor")
print("Pinch thumb + index finger = Click")
print("Press Q to exit")

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to read webcam.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Convert to RGB
    rgb_frame = cv2.cvtColor(
        frame, cv2.COLOR_BGR2RGB
    )

    # Detect hand
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand skeleton
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Index fingertip = 8
            index_tip = hand_landmarks.landmark[8]

            # Thumb fingertip = 4
            thumb_tip = hand_landmarks.landmark[4]

            # Map finger position to screen
            target_x = int(
                index_tip.x * (screen_width - 1)
            )
            target_y = int(
                index_tip.y * (screen_height - 1)
            )

            # Keep cursor within screen
            target_x = max(
                0, min(target_x, screen_width - 1)
            )
            target_y = max(
                0, min(target_y, screen_height - 1)
            )

            # Smooth movement
            current_x = previous_x + (
                target_x - previous_x
            ) * smoothing

            current_y = previous_y + (
                target_y - previous_y
            ) * smoothing

            # Move cursor
            pyautogui.moveTo(
                current_x, current_y
            )

            previous_x = current_x
            previous_y = current_y

            # Finger distance
            distance = math.hypot(
                index_tip.x - thumb_tip.x,
                index_tip.y - thumb_tip.y
            )

            # Pinch to click
            if distance < click_threshold:

                if pinch_released:
                    current_time = time.time()

                    if (
                        current_time - last_click_time
                        > click_cooldown
                    ):
                        pyautogui.click()

                        last_click_time = current_time

                        cv2.putText(
                            frame,
                            "CLICK!",
                            (50, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 255),
                            3
                        )

                pinch_released = False

            elif distance > 0.06:
                pinch_released = True

            # Highlight index finger
            cx = int(index_tip.x * width)
            cy = int(index_tip.y * height)

            cv2.circle(
                frame,
                (cx, cy),
                12,
                (0, 255, 0),
                -1
            )

    else:
        pinch_released = True

    # Instructions on screen
    cv2.putText(
        frame,
        "AIRCTRL - Virtual Mouse",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Index = Move | Pinch = Click | Q = Exit",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "AIRCTRL - Virtual Mouse",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
