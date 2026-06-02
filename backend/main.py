from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from collections import defaultdict
import sqlite3
import json
import os
from datetime import datetime
from ai_engine import (
    analyze_behavior,
    detect_focus_session,
    calculate_score,
    categorize_app
)
from openai_service import generate_ai_coach
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Question(BaseModel):
    question: str


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path (define once)
db_path = os.path.abspath("../tracker/activity.db")

@app.get("/categorized-activities")
def categorized_activities():

    conn=sqlite3.connect(db_path)

    cursor=conn.cursor()

    cursor.execute("""
    SELECT app_name,timestamp
    FROM activity
    ORDER BY id DESC
    LIMIT 15
    """)

    rows=cursor.fetchall()

    conn.close()

    result=[]

    for row in rows:

        result.append({

        "app":row[0],
        "time":row[1],
        "category":categorize_app(row[0])

        })

    return result

@app.get("/activities")
def get_activities():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT app_name, timestamp
        FROM activity
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "app": row[0],
            "time": row[1]
        }
        for row in rows
    ]

@app.get("/download-report")
def download_report():
    return FileResponse(
        "reports/weekly_report.pdf",
        media_type="application/pdf",
        filename="Productivity_Report.pdf"
    )

@app.get("/suggestions")
def get_suggestions():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT app_name
        FROM activity
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()
    conn.close()

    apps = [row[0] for row in rows]

    suggestions = []

    if any("Chrome" in app for app in apps):
        suggestions.append(
            "You spent time browsing → Generate notes?"
        )

    if any("Visual Studio" in app for app in apps):
        suggestions.append(
            "You coded recently → Commit changes?"
        )

    if any("Gmail" in app for app in apps):
        suggestions.append(
            "Emails detected → Create follow-up reminder?"
        )

    return suggestions
@app.get("/ai-insights")
def ai_insights():

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT app_name,timestamp
    FROM activity
    ORDER BY id DESC
    LIMIT 100
    """)

    rows = cursor.fetchall()

    conn.close()

    behavior = analyze_behavior(rows)

    focus = detect_focus_session(rows)

    return {
        "behavior": behavior,
        "focus": focus
    }
    
@app.get("/daily-summary")
def daily_summary():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT app_name
    FROM activity
    ORDER BY id DESC
    LIMIT 100
    """)

    rows = cursor.fetchall()

    conn.close()

    behavior = analyze_behavior(rows)

    counts = behavior["counts"]

    total = sum(counts.values())

    coding = counts.get("Coding", 0)
    research = counts.get("Research", 0)
    email = counts.get("Email", 0)

    summary = (
        f"Tracked {total} recent activities. "
        f"Research accounted for {research} activities, "
        f"coding for {coding}, and email for {email}. "
    )

    if research > coding:
        summary += (
            "Most work involved information gathering rather than implementation."
        )
    else:
        summary += (
            "Implementation activity remained strong throughout the session."
        )

    return {
        "summary": summary
    }
    
@app.get("/productivity-score")
def productivity_score():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT app_name
    FROM activity
    """)

    rows = cursor.fetchall()

    conn.close()

    apps=[row[0] for row in rows]

    score=100

    browsing=sum(
        1 for app in apps
        if "Chrome" in app
    )

    coding=sum(
        1 for app in apps
        if "Visual Studio" in app
    )

    if browsing > coding:
        score -= 20

    if len(apps) > 50:
        score -= 10

    alerts=[]

    if browsing > coding:
        alerts.append(
            "High browsing activity detected"
        )

    if len(apps)>30:
        alerts.append(
            "Frequent app switching detected"
        )

    return {
        "score":score,
        "alerts":alerts
    }
    

@app.get("/live-status")
def live_status():

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT app_name,timestamp
    FROM activity
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if not row:
        return {
            "app": "No Activity",
            "time": "",
            "category": "Other"
        }

    return {
        "app": row[0],
        "time": row[1],
        "category": categorize_app(row[0])
    }
    
@app.get("/current-app")
def current_app():

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT app_name,timestamp
    FROM activity
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if not row:
        return {
            "app": "No Activity",
            "title": "",
            "category": "Other"
        }

    app_name = row[0]

    if " - " in app_name:

        title, app = app_name.split(" - ", 1)

    else:

        title = app_name
        app = app_name

    return {
        "app": app,
        "title": title,
        "category": categorize_app(app_name)
    }
    
@app.get("/")
def root():
    return {"status": "Backend Running"}

    
@app.get("/hourly-activity")
def hourly_activity():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT timestamp
    FROM activity
    ORDER BY id DESC
    LIMIT 500
    """)

    rows = cursor.fetchall()

    conn.close()

    hours = defaultdict(int)

    for row in rows:

        try:
            dt = datetime.fromisoformat(row[0])

            hour = dt.strftime("%H")

            hours[hour] += 1

        except:
            pass

    return dict(hours)

@app.get("/ai-coach")
def ai_coach():

    return {
        "summary": "AI temporarily disabled.",
        "assessment": "Waiting for local AI setup.",
        "recommendations": [
            "Install Ollama",
            "Connect local model",
            "Enable AI workflows"
        ]
    }

@app.post("/n8n-log")
def n8n_log(data: dict):

    print(data)

    return {
        "status": "received"
    }
    
        
@app.post("/ask-ai")
def ask_ai(payload: Question):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT app_name,timestamp
    FROM activity
    ORDER BY id DESC
    LIMIT 100
    """)

    rows = cursor.fetchall()

    conn.close()

    behavior = analyze_behavior(rows)

    prompt = f"""
You are an AI productivity coach.

User question:
{payload.question}

Productivity data:
{behavior}

Answer the user's question using only the data provided.
Be concise and actionable.
"""

    response = generate_ai_coach(prompt)

    return {
        "response": response
    }

from pydantic import BaseModel
import sqlite3

class Activity(BaseModel):
    app_name: str
    timestamp: str

@app.post("/log-activity")
def log_activity(activity: Activity):

    conn = sqlite3.connect("activity.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO activity (app_name, timestamp)
        VALUES (?, ?)
    """, (
        activity.app_name,
        activity.timestamp
    ))

    conn.commit()
    conn.close()

    return {"status": "saved"}