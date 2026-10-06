@echo off
setlocal

if "%~1"=="" (
  echo Usage: prepare-workshop.bat OUTPUT_DIR [GIT_REF]
  exit /b 2
)

set "AMJC_REF=%~2"
if "%AMJC_REF%"=="" set "AMJC_REF=HEAD"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Prepare-WorkshopContent.ps1" -OutputDir "%~1" -Ref "%AMJC_REF%"
exit /b %ERRORLEVEL%
