@echo off
setlocal EnableExtensions

set "RIMWORLD_DIR=%~1"
if not defined RIMWORLD_DIR set "RIMWORLD_DIR=D:\SteamLibrary\steamapps\common\RimWorld"

set "STEAMAPPS=%RIMWORLD_DIR%\..\.."
set "MO_ROOT=%STEAMAPPS%\workshop\content\294100\3219596926"

echo Checking installed Medieval Overhaul source...
if not exist "%MO_ROOT%\About\About.xml" (
    echo [ERROR] Medieval Overhaul was not found:
    echo         %MO_ROOT%
    exit /b 1
)
echo [OK] Medieval Overhaul source is installed.

echo.
echo Validating AMJ Stage A XML against the installed Medieval Overhaul 1.6 source...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Validate-StageA.ps1" ^
    -RepositoryRoot "%~dp0." ^
    -MedievalOverhaulRoot "%MO_ROOT%"
if errorlevel 1 exit /b 1

echo.
echo Running isolated RimWorld/Pickle Stage A integration tests...
call "%~dp0run-e2e.bat" "%RIMWORLD_DIR%"
exit /b %ERRORLEVEL%
