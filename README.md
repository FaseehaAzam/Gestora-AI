

# Gestora AI — Hand Gesture Control System

**Control Beyond Touch**

Gestora AI is a Python-based computer vision application that allows users to control their computers using hand gestures captured through a webcam.

The system uses MediaPipe for real-time hand tracking, OpenCV for video processing, and PyAutoGUI for mouse and keyboard automation.

It includes a desktop dashboard built with Tkinter, allowing users to launch and manage multiple gesture-based features from one interface.

## Features

### 1. Virtual Mouse and Scrolling

- Move the mouse cursor using your index finger.
- Perform left clicks using a thumb-index pinch.
- Scroll webpages using two raised fingers.
- Interact with your computer without a physical mouse.

### 2. Air Drawing

- Draw virtually using your index finger.
- Pause drawing using two fingers.
- Press `C` to clear the canvas.
- Press `S` to save your drawing as a PNG image.
- Press `Q` to exit the drawing window.

### 3. Hand Gesture Recognition

Recognizes five hand gestures:

- Open Palm
- Fist
- Peace
- Thumbs Up
- Pointing

The system identifies gestures using hand landmark positions and rule-based finger detection.

### 4. Presentation Control

Control presentation slides using hand gestures.

| Gesture | Action |
|---------|--------|
| Peace | Next slide |
| Fist | Previous slide |
| Open Palm | Reset / Ready for next gesture |

The presentation controller includes gesture stability checks and a cooldown mechanism to reduce accidental slide changes.

### 5. Desktop Dashboard

A user-friendly graphical interface developed using Tkinter.

The dashboard provides:

- Virtual Mouse + Scroll
- Air Drawing
- Presentation Control
- Gesture Recognition
- Stop Current Feature
- Real-time feature status

Only one gesture-control feature can run at a time through the dashboard.

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Main programming language |
| OpenCV | Webcam capture and image processing |
| MediaPipe | Hand landmark detection |
| PyAutoGUI | Mouse and keyboard automation |
| NumPy | Numerical operations |
| Tkinter | Desktop graphical interface |

## How Gestora AI Works

1. The webcam captures live video frames.
2. OpenCV processes the frames.
3. MediaPipe detects 21 landmarks on the hand.
4. Python analyzes finger positions and movements.
5. Rule-based gesture recognition determines the action.
6. PyAutoGUI executes the corresponding mouse or keyboard command.

**Technical Note:** Gestora AI uses MediaPipe's pretrained hand landmark detection model. The gesture classification logic is currently rule-based, rather than a separately trained custom machine learning model.

## Installation

### Prerequisites

- Python 3.11
- A working webcam
- Windows operating system
- Git (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/FaseehaAzam/Gestora-AI.git
cd Gestora-AI
```

Alternatively, download the repository as a ZIP file and extract it.

### Step 2: Create a Virtual Environment

Open Command Prompt inside the project folder.

```cmd
py -3.11 -m venv gestora_env
```

Activate the environment:

```cmd
gestora_env\Scripts\activate
```

### Step 3: Install Dependencies

```cmd
python -m pip install -r requirements.txt
```

## Run the Application

Start the main dashboard:

```cmd
python dashboard.py
```

The Gestora AI dashboard will open.

Select a feature to start using hand gestures.

To stop a running feature, click **STOP CURRENT FEATURE**.

## Run Individual Features

You can also run each module separately.

### Hand Tracking

```cmd
python hand_tracking.py
```

### Virtual Mouse

```cmd
python virtual_mouse.py
```

### Virtual Mouse and Scrolling

```cmd
python airctrl_scroll.py
```

### Air Drawing

```cmd
python air_drawing.py
```

### Gesture Recognition

```cmd
python gesture_recognition.py
```

### Presentation Control

```cmd
python gesture_shortcuts.py
```

## Project Structure

```text
Gestora-AI/
|
|-- dashboard.py
|-- camera_test.py
|-- hand_tracking.py
|-- virtual_mouse.py
|-- airctrl_scroll.py
|-- air_drawing.py
|-- gesture_recognition.py
|-- gesture_shortcuts.py
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## Application Controls

| Feature | Gesture / Key | Action |
|---------|---------------|--------|
| Virtual Mouse | Index finger | Move cursor |
| Virtual Mouse | Thumb-index pinch | Left click |
| Scrolling | Two raised fingers | Scroll |
| Air Drawing | Index finger | Draw |
| Air Drawing | Index + middle fingers | Pause |
| Air Drawing | C | Clear drawing |
| Air Drawing | S | Save drawing |
| Air Drawing | Q | Quit |
| Presentation | Peace | Next slide |
| Presentation | Fist | Previous slide |
| Presentation | Open Palm | Reset / Ready |

## System Requirements

- Webcam with adequate lighting
- Python 3.11
- Windows 10 or 11
- Required Python libraries installed
- Sufficient processing power for real-time video analysis

Performance may vary depending on webcam quality, lighting, and computer hardware.

## Limitations

- Gesture recognition accuracy depends on hand visibility and lighting.
- Rapid hand movements may affect tracking stability.
- Some gestures may be confused due to hand orientation.
- Performance can decrease on lower-powered devices.
- The current gesture recognition system uses predefined rules.

## Future Improvements

- Train a custom machine learning gesture classifier.
- Improve gesture recognition accuracy.
- Add customizable gesture shortcuts.
- Introduce adjustable sensitivity settings.
- Improve real-time processing performance.
- Add more accessibility-focused features.
- Enhance the graphical user interface.

## Learning Outcomes

This project provided practical experience in:

- Computer vision
- Real-time hand tracking
- Human-computer interaction
- Gesture recognition
- Python GUI development
- Mouse and keyboard automation
- Integrating multiple Python modules
- Git and GitHub version control

## Author

**FaseehaAzam**

AI Student | Python | Computer Vision | Machine Learning

GitHub: https://github.com/FaseehaAzam

## Repository

https://github.com/FaseehaAzam/Gestora-AI

## License

No license has been selected for this project.
