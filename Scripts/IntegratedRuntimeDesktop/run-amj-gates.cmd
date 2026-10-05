@echo off
setlocal EnableExtensions
set "PSModulePath=%SystemRoot%\System32\WindowsPowerShell\v1.0\Modules"
cd /d "D:\SteamLibrary\steamapps\common\RimWorld\Mods\AncientMedievalJapanCore"
call run-e2e.bat
if errorlevel 1 exit /b 1
cd /d "D:\SteamLibrary\steamapps\common\RimWorld\Mods\AncientMedievalJapanEnvironment"
call run-runtime-tests.bat
exit /b %ERRORLEVEL%
