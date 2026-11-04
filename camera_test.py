
import cv2

# Open laptop webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam!")
    exit()

print("Webcam started successfully!")

while True:
    success, frame = cap.read()

    if not success:
        print("Cannot read webcam frame!")
        break

    cv2.imshow("AIRCTRL - Webcam Test", frame)

    # Press Q to close webcam
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
