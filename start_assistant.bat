@echo off

start "Backend" cmd /k "cd /d D:\AI Work Assistant\backend && D:\AI Work Assistant\.venv\Scripts\python.exe -m uvicorn main:app --reload"

start "Tracker" cmd /k "cd /d D:\AI Work Assistant\tracker && D:\AI Work Assistant\.venv\Scripts\python.exe app_tracker.py"

start "Frontend" cmd /k "cd /d D:\AI Work Assistant\frontend && npm run dev"

timeout /t 8 >nul

start "Tray" cmd /k "cd /d D:\AI Work Assistant\tracker && D:\AI Work Assistant\.venv\Scripts\python.exe tray_app.py"