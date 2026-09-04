import os
import sys

desktop_paths = [
    os.path.expanduser("~/OneDrive/Desktop"),
    os.path.expanduser("~/Desktop")
]

bat_content = """@echo off
title FixOrPro 3.0 AI App
cd /d "c:\\Users\\loveh\\1인 기업"

echo Starting FixOrPro 3.0 AI App Server...
echo Web browser will open automatically when server is ready.
echo.

start /b powershell -NoProfile -ExecutionPolicy Bypass -Command "$maxRetries=30; for ($i=0; $i -lt $maxRetries; $i++) { Start-Sleep -Milliseconds 500; try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing -TimeoutSec 1; if ($res.StatusCode -eq 200) { Start-Process 'http://127.0.0.1:8000'; break } } catch {} }"

".venv\\Scripts\\python.exe" -m app.main
"""

url_content = """[InternetShortcut]
URL=http://127.0.0.1:8000
IconFile=C:\\Windows\\System32\\shell32.dll
IconIndex=277
"""

for desktop in desktop_paths:
    if os.path.exists(desktop):
        bat_path = os.path.join(desktop, "FixOrPro_AI_App_Start.bat")
        with open(bat_path, "wb") as f:
            f.write(bat_content.encode("utf-8"))

        bat_path2 = os.path.join(desktop, "FixOrPro AI 집수리 앱 실행.bat")
        with open(bat_path2, "wb") as f:
            f.write(bat_content.encode("utf-8"))

        url_path = os.path.join(desktop, "FixOrPro_AI_App.url")
        with open(url_path, "wb") as f:
            f.write(url_content.encode("utf-8"))

print("All shortcuts updated successfully!")
