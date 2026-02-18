$startup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$shortcut = Join-Path $startup "NovaAssistant.lnk"
$wshell = New-Object -ComObject WScript.Shell
$lnk = $wshell.CreateShortcut($shortcut)
$lnk.TargetPath = (Resolve-Path "autostart.bat")
$lnk.WorkingDirectory = (Get-Location).Path
$lnk.Save()
Write-Output "Added autostart shortcut at $shortcut"
