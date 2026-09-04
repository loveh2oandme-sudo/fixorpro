$Wss = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")

$ShortcutPath = System.IO.Path::Combine($DesktopPath, "FixOrPro AI Home Repair.lnk")
$Shortcut = $Wss.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "c:\Users\loveh\1인 기업\run_app.bat"
$Shortcut.WorkingDirectory = "c:\Users\loveh\1인 기업"
$Shortcut.Description = "FixOrPro 3.0 AI Home Repair App"
$Shortcut.IconLocation = "shell32.dll,277"
$Shortcut.Save()

# Also create Korean named shortcut file
$ShortcutPathKo = System.IO.Path::Combine($DesktopPath, "FixOrPro_AI_집수리_앱.lnk")
$Shortcut2 = $Wss.CreateShortcut($ShortcutPathKo)
$Shortcut2.TargetPath = "c:\Users\loveh\1인 기업\run_app.bat"
$Shortcut2.WorkingDirectory = "c:\Users\loveh\1인 기업"
$Shortcut2.IconLocation = "shell32.dll,277"
$Shortcut2.Save()

Write-Host "Desktop shortcuts created successfully!"
