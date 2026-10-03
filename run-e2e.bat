@echo off
setlocal EnableExtensions

set "RIMWORLD_DIR=%~1"
if not defined RIMWORLD_DIR set "RIMWORLD_DIR=D:\SteamLibrary\steamapps\common\RimWorld"

set "ROOT=%~dp0"
set "RIMWORLD_EXE=%RIMWORLD_DIR%\RimWorldWin64.exe"
set "REPORT_DIR=%ROOT%TestResults\Pickle"
set "TEST_SAVEDATA=%ROOT%TestResults\SaveData"

echo.
echo Resetting isolated AMJ test output...
if exist "%REPORT_DIR%" rmdir /S /Q "%REPORT_DIR%"
if errorlevel 1 exit /b 1
if exist "%TEST_SAVEDATA%" rmdir /S /Q "%TEST_SAVEDATA%"
if errorlevel 1 exit /b 1

call "%ROOT%build-e2e.bat" "%RIMWORLD_DIR%"
if errorlevel 1 exit /b 1

if not exist "%RIMWORLD_EXE%" (
    echo [ERROR] RimWorld executable was not found:
    echo         %RIMWORLD_EXE%
    exit /b 1
)

echo.
echo Preparing isolated RimWorld test profile...
powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT%Scripts\Prepare-TestSaveData.ps1" ^
    -OutputRoot "%TEST_SAVEDATA%"
if errorlevel 1 exit /b 1

if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

echo.
echo Running AMJ Stage A Pickle suite...
echo Feature filter: stage-a.feature
echo Report: %REPORT_DIR%
echo Isolated save data: %TEST_SAVEDATA%
echo The normal RimWorld mod list is not changed.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT%Scripts\Run-RimWorldWithTimeout.ps1" ^
    -ExePath "%RIMWORLD_EXE%" ^
    -SavedataFolder "%TEST_SAVEDATA%" ^
    -ReportDir "%REPORT_DIR%" ^
    -RunFilter "stage-a.feature" ^
    -TimeoutSeconds 300

set "RESULT=%ERRORLEVEL%"

if "%RESULT%"=="0" (
    echo.
    echo Verifying fresh AMJ Pickle summary...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT%Scripts\Validate-PickleSummary.ps1" ^
        -SummaryPath "%REPORT_DIR%\summary.json"
    if errorlevel 1 set "RESULT=2"
)

echo.
if "%RESULT%"=="0" (
    echo [OK] AMJ Stage A automated gate passed.
) else if "%RESULT%"=="1" (
    echo [FAIL] One or more AMJ Pickle scenarios failed.
) else if "%RESULT%"=="2" (
    echo [ERROR] AMJ Pickle runner failed or the expected scenarios were not produced.
) else if "%RESULT%"=="124" (
    echo [ERROR] RimWorld/Pickle was terminated by the outer 5-minute watchdog.
) else (
    echo [ERROR] RimWorld/Pickle exited with code %RESULT%.
)

echo Report directory:
echo   %REPORT_DIR%
exit /b %RESULT%
