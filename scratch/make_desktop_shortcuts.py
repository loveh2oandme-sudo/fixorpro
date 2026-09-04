import os
import subprocess

desktop_paths = [
    os.path.expanduser("~/OneDrive/Desktop"),
    os.path.expanduser("~/Desktop")
]

bat_content = """@echo off
chcp 65001 > nul
title FixOrPro 3.0 AI 집수리 앱
echo ========================================================
echo   FixOrPro 3.0 AI 집수리 모바일/웹 앱을 실행 중입니다...
echo   웹 브라우저가 자동으로 열립니다: http://127.0.0.1:8000
echo ========================================================
echo.
timeout /t 2 /nobreak > nul
start http://127.0.0.1:8000
cd /d "c:\\Users\\loveh\\1인 기업"
".venv\\Scripts\\python.exe" app/main.py
"""

url_content = """[InternetShortcut]
URL=http://127.0.0.1:8000
IDList=
IconFile=C:\\Windows\\System32\\shell32.dll
IconIndex=277
"""

for desktop in desktop_paths:
    if os.path.exists(desktop):
        # Create .bat shortcut
        bat_file = os.path.join(desktop, "FixOrPro AI 집수리 앱 실행.bat")
        with open(bat_file, "w", encoding="utf-8") as f:
            f.write(bat_content)
        print(f"Created: {bat_file}")

        # Create .url shortcut
        url_file = os.path.join(desktop, "FixOrPro AI 집수리 앱.url")
        with open(url_file, "w", encoding="utf-8") as f:
            f.write(url_content)
        print(f"Created: {url_file}")

# Also use PowerShell COM object to make proper .lnk file
ps_script = """
$ws = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath('Desktop')
$lnkPath = Join-Path $desktop 'FixOrPro AI 집수리.lnk'
$shortcut = $ws.CreateShortcut($lnkPath)
$shortcut.TargetPath = 'c:\\Users\\loveh\\1인 기업\\run_app.bat'
$shortcut.WorkingDirectory = 'c:\\Users\\loveh\\1인 기업'
$shortcut.Description = 'FixOrPro 3.0 AI 1:1 집수리 앱'
$shortcut.IconLocation = 'C:\\Windows\\System32\\shell32.dll,277'
$shortcut.Save()
"""

try:
    subprocess.run(["powershell", "-Command", ps_script], check=True)
    print("PowerShell LNK created successfully!")
except Exception as e:
    print(f"LNK creation error: {e}")
