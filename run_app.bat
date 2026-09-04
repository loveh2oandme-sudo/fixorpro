@echo off
title FixOrPro 3.0 AI App
cd /d "c:\Users\loveh\1인 기업"

echo Starting FixOrPro 3.0 AI App Server...
echo Web browser will open automatically when server is ready.
echo.

start /b powershell -NoProfile -ExecutionPolicy Bypass -Command "$maxRetries=30; for ($i=0; $i -lt $maxRetries; $i++) { Start-Sleep -Milliseconds 500; try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing -TimeoutSec 1; if ($res.StatusCode -eq 200) { Start-Process 'http://127.0.0.1:8000'; break } } catch {} }"

".venv\Scripts\python.exe" -m app.main
