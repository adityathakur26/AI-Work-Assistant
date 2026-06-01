import threading
import subprocess
import webview
import time
import webbrowser

from pystray import Icon, MenuItem, Menu
from PIL import Image

import os


backend_process = None
tracker_process = None

print("TRAY APP STARTED")


def open_dashboard(icon=None, item=None):

    time.sleep(5)

    webview.create_window(
        "AI Work Assistant",
        "http://127.0.0.1:8000",
        width=1400,
        height=900
    )

    webview.start()


def quit_app(icon, item):

    global backend_process
    global tracker_process

    if backend_process:
        backend_process.terminate()

    if tracker_process:
        tracker_process.terminate()

    icon.stop()

def start_services():

    global backend_process
    global tracker_process

    BASE_DIR = r"D:\AI Work Assistant"
    PYTHON_EXE = r"D:\AI Work Assistant\.venv\Scripts\python.exe"

    print("BASE_DIR =", BASE_DIR)
    print("PYTHON_EXE =", PYTHON_EXE)

    try:
        backend_process = subprocess.Popen(
            [
                PYTHON_EXE,
                "-m",
                "uvicorn",
                "main:app"
            ],
            cwd=rf"{BASE_DIR}\backend"
        )
        print("Backend started")
    except Exception as e:
        print("Backend error:", e)

    try:
        tracker_process = subprocess.Popen(
            [
                PYTHON_EXE,
                "app_tracker.py"
            ],
            cwd=rf"{BASE_DIR}\tracker"
        )
        print("Tracker started")
    except Exception as e:
        print("Tracker error:", e)
        
def create_tray():
    print("CREATING TRAY")

    from PIL import Image

    image = Image.new("RGB", (64,64), (255,0,0))

    menu = Menu(

        MenuItem(
            "Open Dashboard",
            open_dashboard
        ),

        MenuItem(
            "Exit",
            quit_app
        )

    )

    icon = Icon(
        "AI Work Assistant",
        image,
        "AI Work Assistant",
        menu
    )

    print("RUNNING TRAY ICON")
    icon.run()


if __name__ == "__main__":

    threading.Thread(
        target=start_services,
        daemon=True
    ).start()

    time.sleep(5)
    webbrowser.open(
        "http://127.0.0.1:8000"
    )

    create_tray()