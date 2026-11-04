\# Gestora AI — AI-Powered Hand Gesture Control System



\*\*Control your computer without touching a mouse or keyboard!\*\*



Gestora AI is a Python-based computer vision application that uses a webcam to detect hand movements and recognize gestures in real time.



It provides a desktop dashboard for launching different touchless interaction features.



\## Features



\### 1. Virtual Mouse

\- Move the mouse cursor using your index finger.

\- Perform left clicks using a thumb-index pinch.

\- Scroll webpages using two raised fingers.



\### 2. Air Drawing

\- Draw in the air using your index finger.

\- Pause drawing using two fingers.

\- Clear the canvas by pressing `C`.

\- Save drawings as PNG images by pressing `S`.



\### 3. Gesture Recognition

Recognizes hand gestures including:

\- Open Palm

\- Fist

\- Peace

\- Thumbs Up

\- Pointing



\### 4. Presentation Control

Control PowerPoint presentations using hand gestures:

\- Peace: Next slide

\- Fist: Previous slide

\- Open Palm: Reset gesture



\### 5. Desktop Dashboard

A Tkinter-based graphical interface for launching and stopping different Gestora AI features.



\## Technologies Used



\- Python 3.11

\- OpenCV

\- MediaPipe

\- PyAutoGUI

\- NumPy

\- Tkinter



\## How It Works



1\. The webcam captures live video.

2\. MediaPipe detects hand landmarks.

3\. Python analyzes fingertip positions and hand gestures.

4\. Gesture rules determine the requested action.

5\. PyAutoGUI performs mouse or keyboard operations.



\*\*Note:\*\* Gesture recognition currently uses landmark-based rules rather than a separately trained machine learning classifier.



\## Installation



\### 1. Clone the repository



```bash

git clone https://github.com/FaseehaAzam/Gestora-AI.git

cd Gestora-AI

```



\### 2. Create a virtual environment



On Windows:



```cmd

py -3.11 -m venv gestora\_env

gestora\_env\\Scripts\\activate

```



\### 3. Install dependencies



```bash

python -m pip install -r requirements.txt

```



\## Run the Application



```bash

python dashboard.py

```



Select a feature from the dashboard.



\## Project Files



\- `dashboard.py` — Main desktop dashboard

\- `camera\_test.py` — Webcam testing

\- `hand\_tracking.py` — Hand landmark detection

\- `virtual\_mouse.py` — Mouse movement and clicking

\- `airctrl\_scroll.py` — Mouse movement, clicking, and scrolling

\- `air\_drawing.py` — Virtual drawing canvas

\- `gesture\_recognition.py` — Gesture recognition

\- `gesture\_shortcuts.py` — Presentation control

\- `requirements.txt` — Python dependencies

\- `.gitignore` — Files excluded from version control



\## Notes



\- A working webcam is required.

\- Performance depends on hardware and lighting.

\- Only one webcam feature should run at a time.

\- Gesture recognition may vary with hand orientation.



\## Future Improvements



\- Custom-trained gesture classification model

\- More keyboard shortcuts

\- Adjustable gesture sensitivity

\- Improved graphical interface

\- Performance optimization



\## Author



\*\*FaseehaAzam\*\*



GitHub: https://github.com/FaseehaAzam



\## License



No license has been selected yet.



