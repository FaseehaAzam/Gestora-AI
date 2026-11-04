

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Gestora AI - Main Dashboard

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
running_process = None

BG = "#0f172a"
TEXT = "#cbd5e1"
MUTED = "#94a3b8"
ACCENT = "#38bdf8"


def launch_feature(filename, feature_name):
    global running_process

    if running_process and running_process.poll() is None:
        messagebox.showwarning(
            "Gestora AI",
            "Please stop the current feature first."
        )
        return

    script_path = os.path.join(BASE_DIR, filename)

    if not os.path.isfile(script_path):
        messagebox.showerror(
            "File Missing",
            f"Cannot find {filename}"
        )
        return

    try:
        running_process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=BASE_DIR
        )

        status_label.config(
            text=f"Running: {feature_name}",
            fg="#22c55e"
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            str(error)
        )


def stop_feature():
    global running_process

    if running_process and running_process.poll() is None:
        running_process.terminate()

        try:
            running_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            running_process.kill()
            running_process.wait()

    running_process = None

    status_label.config(
        text="Status: Ready",
        fg=MUTED
    )


def close_dashboard():
    stop_feature()
    root.destroy()


root = tk.Tk()
root.title("Gestora AI | Hand Gesture Control")
root.geometry("500x620")
root.configure(bg=BG)
root.resizable(False, False)


# Main heading
title = tk.Label(
    root,
    text="GESTORA AI",
    font=("Segoe UI", 30, "bold"),
    fg=ACCENT,
    bg=BG
)
title.pack(pady=(28, 5))


# Subtitle
subtitle = tk.Label(
    root,
    text="AI-Powered Touchless Computer Control",
    font=("Segoe UI", 11),
    fg=TEXT,
    bg=BG
)
subtitle.pack(pady=(0, 8))


tagline = tk.Label(
    root,
    text="Control Beyond Touch",
    font=("Segoe UI", 10, "italic"),
    fg=MUTED,
    bg=BG
)
tagline.pack(pady=(0, 20))


def add_button(text, filename, color):
    button = tk.Button(
        root,
        text=text,
        font=("Segoe UI", 12, "bold"),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=29,
        height=2,
        command=lambda: launch_feature(filename, text)
    )
    button.pack(pady=7)


# Features
add_button(
    "Virtual Mouse + Scroll",
    "airctrl_scroll.py",
    "#2563eb"
)

add_button(
    "Air Drawing",
    "air_drawing.py",
    "#7c3aed"
)

add_button(
    "Presentation Control",
    "gesture_shortcuts.py",
    "#0891b2"
)

add_button(
    "Gesture Recognition",
    "gesture_recognition.py",
    "#0d9488"
)


# Stop button
stop_button = tk.Button(
    root,
    text="STOP CURRENT FEATURE",
    font=("Segoe UI", 11, "bold"),
    bg="#dc2626",
    fg="white",
    activebackground="#b91c1c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=29,
    height=2,
    command=stop_feature
)
stop_button.pack(pady=(20, 10))


# Status label
status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Segoe UI", 10),
    fg=MUTED,
    bg=BG
)
status_label.pack(pady=7)


# Footer
footer = tk.Label(
    root,
    text="Powered by Python | OpenCV | MediaPipe",
    font=("Segoe UI", 9),
    fg="#64748b",
    bg=BG
)
footer.pack(side="bottom", pady=14)


root.protocol("WM_DELETE_WINDOW", close_dashboard)
root.mainloop()
