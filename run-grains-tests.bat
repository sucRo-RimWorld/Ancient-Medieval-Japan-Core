@echo off
setlocal EnableExtensions
set "RIMWORLD_DIR=%~1"
if not defined RIMWORLD_DIR set "RIMWORLD_DIR=D:\SteamLibrary\steamapps\common\RimWorld"
set "PROFILE=%~2"
if not defined PROFILE set "PROFILE=all"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\IntegratedRuntimeDesktop\Run-AMJ-IsolatedDesktop.ps1" ^
    -Grains -RimWorldRoot "%RIMWORLD_DIR%" -GrainsProfile "%PROFILE%" -TimeoutSeconds 2400
exit /b %ERRORLEVEL%
