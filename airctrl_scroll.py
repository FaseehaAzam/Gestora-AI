

import cv2
import mediapipe as mp
import pyautogui
import math
import time

# ==============================
# AIRCTRL - AI Gesture Control
# Optimized Version
# ==============================

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Screen dimensions
screen_w, screen_h = pyautogui.size()

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam not found!")
    hands.close()
    raise SystemExit

# Reduce webcam processing load
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Mouse settings
prev_x, prev_y = pyautogui.position()
smoothing = 0.25

# Click settings
pinch_ready = True
last_click = 0
click_cooldown = 0.5

# Scroll settings
scroll_prev_y = None
scroll_sensitivity = 500
scroll_threshold = 0.008

print("AIRCTRL Started!")
print("Index finger = Move cursor")
print("Thumb + Index = Click")
print("Index + Middle = Scroll")
print("Press Q to exit")

try:
    while True:
        success, frame = cap.read()

        if not success:
            print("Cannot read webcam frame.")
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Convert to RGB
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Improve processing performance
        rgb.flags.writeable = False
        result = hands.process(rgb)
        rgb.flags.writeable = True

        mode = "NO HAND"

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]

            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand.landmark

            # Fingertips
            thumb = lm[4]
            index = lm[8]
            middle = lm[12]

            # Finger positions
            index_up = lm[8].y < lm[6].y
            middle_up = lm[12].y < lm[10].y
            ring_down = lm[16].y > lm[14].y
            pinky_down = lm[20].y > lm[18].y

            # Pinch distance
            pinch_distance = math.hypot(
                thumb.x - index.x,
                thumb.y - index.y
            )

            # Scroll gesture detection
            scroll_mode = (
                index_up
                and middle_up
                and ring_down
                and pinky_down
            )

            if scroll_mode:
                mode = "FAST SCROLL"

                current_y = (
                    index.y + middle.y
                ) / 2

                if scroll_prev_y is not None:
                    difference = (
                        scroll_prev_y - current_y
                    )

                    if abs(difference) > scroll_threshold:
                        amount = int(
                            difference * scroll_sensitivity
                        )

                        if amount != 0:
                            pyautogui.scroll(amount)

                scroll_prev_y = current_y
                pinch_ready = False

            else:
                scroll_prev_y = None

                # Convert finger coordinates
                target_x = int(
                    index.x * (screen_w - 1)
                )

                target_y = int(
                    index.y * (screen_h - 1)
                )

                # Keep cursor inside screen
                target_x = max(
                    0, min(target_x, screen_w - 1)
                )

                target_y = max(
                    0, min(target_y, screen_h - 1)
                )

                # Smooth cursor movement
                current_x = prev_x + (
                    target_x - prev_x
                ) * smoothing

                current_y = prev_y + (
                    target_y - prev_y
                ) * smoothing

                pyautogui.moveTo(
                    current_x,
                    current_y
                )

                prev_x = current_x
                prev_y = current_y

                mode = "MOUSE MOVE"

                # Pinch-to-click
                if pinch_distance < 0.04:
                    mode = "PINCH"

                    if pinch_ready:
                        now = time.time()

                        if now - last_click > click_cooldown:
                            pyautogui.click()
                            last_click = now
                            mode = "CLICK!"

                    pinch_ready = False

                elif pinch_distance > 0.06:
                    pinch_ready = True

            # Highlight index fingertip
            cx = int(index.x * w)
            cy = int(index.y * h)

            cv2.circle(
                frame,
                (cx, cy),
                10,
                (0, 255, 0),
                -1
            )

        else:
            scroll_prev_y = None
            pinch_ready = True

        # Display interface
        cv2.putText(
            frame,
            "AIRCTRL - AI Gesture Control",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "MODE: " + mode,
            (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Index: Move | Pinch: Click | V: Scroll",
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "AIRCTRL - Optimized Gesture Control",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except pyautogui.FailSafeException:
    print("Safety stop activated!")

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    cap.release()
    hands.close()
    cv2.destroyAllWindows()
