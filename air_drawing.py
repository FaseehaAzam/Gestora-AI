
import cv2
import mediapipe as mp
import numpy as np

# AIRCTRL - Air Drawing

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

canvas = None
previous_point = None

brush_color = (255, 0, 255)
brush_thickness = 5

print("AIRCTRL Air Drawing Started!")
print("Index finger = Draw")
print("Index + Middle = Pause drawing")
print("C = Clear")
print("S = Save")
print("Q = Exit")

try:
    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]

        # Create drawing canvas
        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        result = hands.process(rgb)

        mode = "WAITING"

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand.landmark

            index_up = lm[8].y < lm[6].y
            middle_up = lm[12].y < lm[10].y

            x = int(lm[8].x * width)
            y = int(lm[8].y * height)

            x = max(0, min(x, width - 1))
            y = max(0, min(y, height - 1))

            if index_up and not middle_up:
                mode = "DRAWING"

                if previous_point is not None:
                    cv2.line(
                        canvas,
                        previous_point,
                        (x, y),
                        brush_color,
                        brush_thickness
                    )

                previous_point = (x, y)

                cv2.circle(
                    frame,
                    (x, y),
                    10,
                    (0, 255, 0),
                    -1
                )

            else:
                mode = "PAUSED"
                previous_point = None

        else:
            previous_point = None

        # Combine webcam and drawing
        output = cv2.addWeighted(
            frame,
            1.0,
            canvas,
            1.0,
            0
        )

        cv2.putText(
            output,
            "AIRCTRL - AIR DRAWING",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            output,
            "MODE: " + mode,
            (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            output,
            "C: Clear | S: Save | Q: Exit",
            (10, height - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "AIRCTRL - Air Drawing",
            output
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("c"):
            canvas[:] = 0
            previous_point = None
            print("Canvas cleared!")

        elif key == ord("s"):
            filename = "airctrl_drawing.png"

            # Save drawing on a white background
            white_canvas = np.full_like(
                canvas, 255
            )

            mask = np.any(canvas != 0, axis=2)
            white_canvas[mask] = canvas[mask]

            cv2.imwrite(
                filename,
                white_canvas
            )

            print("Drawing saved:", filename)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    cap.release()
    hands.close()
    cv2.destroyAllWindows()
