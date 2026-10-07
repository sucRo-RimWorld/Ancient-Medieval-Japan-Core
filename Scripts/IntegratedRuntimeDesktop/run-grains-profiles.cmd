@echo off
setlocal EnableExtensions
set "PSModulePath=%SystemRoot%\System32\WindowsPowerShell\v1.0\Modules"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\Run-GrainsProfiles.ps1" ^
    -RimWorldRoot "%~1" -Profile "%~2"
exit /b %ERRORLEVEL%
