
import cv2
import mediapipe as mp
import pyautogui
import math
import time

# AIRCTRL - Gesture Presentation Controller

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Webcam not found!")
    hands.close()
    raise SystemExit

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def recognize_gesture(lm):
    wrist = lm[0]

    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]

    fingers = []

    for tip, joint in zip(tips, joints):
        extended = (
            distance(lm[tip], wrist)
            > distance(lm[joint], wrist) * 1.12
        )
        fingers.append(extended)

    thumb_open = (
        distance(lm[4], lm[17])
        > distance(lm[3], lm[17]) * 1.12
    )

    index, middle, ring, pinky = fingers

    if index and middle and not ring and not pinky:
        return "PEACE"

    if not any(fingers) and not thumb_open:
        return "FIST"

    if all(fingers) and thumb_open:
        return "OPEN PALM"

    return "UNKNOWN"

# Prevent repeated commands
last_action = 0
cooldown = 1.5
stable_gesture = None
stable_frames = 0
gesture_armed = True

print("AIRCTRL Presentation Control Started!")
print("PEACE = Next slide")
print("FIST = Previous slide")
print("OPEN PALM = Reset gesture")
print("Q = Exit")

try:
    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        result = hands.process(rgb)

        gesture = "NO HAND"

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            gesture = recognize_gesture(hand.landmark)

        # Gesture stability check
        if gesture == stable_gesture:
            stable_frames += 1
        else:
            stable_gesture = gesture
            stable_frames = 1

        if stable_frames >= 6:
            if gesture == "OPEN PALM":
                gesture_armed = True

            elif gesture in ("PEACE", "FIST"):
                now = time.time()

                if gesture_armed and now - last_action > cooldown:
                    if gesture == "PEACE":
                        pyautogui.press("right")
                        print("NEXT SLIDE")

                    elif gesture == "FIST":
                        pyautogui.press("left")
                        print("PREVIOUS SLIDE")

                    last_action = now
                    gesture_armed = False

        # Display status
        cv2.putText(
            frame,
            "AIRCTRL - PRESENTATION CONTROL",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "GESTURE: " + gesture,
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        status = "READY" if gesture_armed else "SHOW OPEN PALM"

        cv2.putText(
            frame,
            status,
            (10, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "AIRCTRL - Presentation Control",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    cap.release()
    hands.close()
    cv2.destroyAllWindows()
