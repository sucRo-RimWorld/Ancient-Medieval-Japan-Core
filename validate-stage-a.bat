@echo off
setlocal EnableExtensions

set "RIMWORLD_DIR=%~1"
if not defined RIMWORLD_DIR set "RIMWORLD_DIR=D:\SteamLibrary\steamapps\common\RimWorld"

set "MO_ROOT=%RIMWORLD_DIR%\..\..\workshop\content\294100\3219596926"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Validate-StageA.ps1" ^
    -RepositoryRoot "%~dp0." ^
    -MedievalOverhaulRoot "%MO_ROOT%" ^
    -RimWorldRoot "%RIMWORLD_DIR%"

exit /b %ERRORLEVEL%
