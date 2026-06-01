import pygetwindow as gw
import time
import sqlite3
from datetime import datetime
from notifier import notify

# Startup notification
notify(
    "AI Work Assistant",
    "Activity tracking started"
)

# Database
conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT,
    timestamp TEXT
)
""")

conn.commit()

last_window = ""

while True:

    try:

        window = gw.getActiveWindow()

        if window and window.title != last_window:

            blocked = [
                "localhost",
                "127.0.0.1",
                "AI Work Assistant",
                "app_tracker.py",
                "tray_app.py"
            ]

            if any(
                item.lower() in window.title.lower()
                for item in blocked
            ):
                time.sleep(5)
                continue

            last_window = window.title

            current_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            print("Current App:", window.title)

            cursor.execute(
                """
                INSERT INTO activity
                (app_name,timestamp)
                VALUES (?,?)
                """,
                (
                    window.title,
                    current_time
                )
            )

            conn.commit()

            title = window.title.lower()

            # AI Work Detection
            if "chatgpt" in title:

                notify(
                    "🧠 AI Work Detected",
                    "Using ChatGPT productively."
                )

            # Coding Detection
            elif (
                "visual studio" in title
                or "vscode" in title
                or "github" in title
            ):

                notify(
                    "💻 Coding Session",
                    "Coding activity detected."
                )

            # Learning Detection
            elif "youtube" in title:

                notify(
                    "📚 Learning Session",
                    "YouTube learning activity detected."
                )

            # Meetings
            elif (
                "zoom" in title
                or "meet" in title
            ):

                notify(
                    "🎥 Meeting Started",
                    "Meeting activity detected."
                )

    except Exception as e:

        print("Error:", e)

    time.sleep(5)