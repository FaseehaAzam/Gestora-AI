
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# AIRCTRL - Main Dashboard

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
running_process = None

def launch_feature(filename):
    global running_process

    if running_process and running_process.poll() is None:
        messagebox.showwarning(
            "AIRCTRL",
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
            text=f"Running: {filename}",
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
        fg="#94a3b8"
    )

def close_dashboard():
    stop_feature()
    root.destroy()

root = tk.Tk()
root.title("AIRCTRL - AI Gesture Control")
root.geometry("480x560")
root.configure(bg="#0f172a")
root.resizable(False, False)

title = tk.Label(
    root,
    text="AIRCTRL",
    font=("Segoe UI", 30, "bold"),
    fg="#38bdf8",
    bg="#0f172a"
)
title.pack(pady=(30, 5))

subtitle = tk.Label(
    root,
    text="AI-Powered Touchless Computer Control",
    font=("Segoe UI", 11),
    fg="#cbd5e1",
    bg="#0f172a"
)
subtitle.pack(pady=(0, 25))

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
        command=lambda: launch_feature(filename)
    )
    button.pack(pady=7)

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

stop_button = tk.Button(
    root,
    text="STOP CURRENT FEATURE",
    font=("Segoe UI", 11, "bold"),
    bg="#dc2626",
    fg="white",
    relief="flat",
    width=29,
    height=2,
    command=stop_feature
)
stop_button.pack(pady=(20, 10))

status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Segoe UI", 10),
    fg="#94a3b8",
    bg="#0f172a"
)
status_label.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", close_dashboard)
root.mainloop()
