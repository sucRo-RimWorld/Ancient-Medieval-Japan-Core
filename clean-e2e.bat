@echo off
setlocal EnableExtensions

set "RIMWORLD_DIR=%~1"
if not defined RIMWORLD_DIR set "RIMWORLD_DIR=D:\SteamLibrary\steamapps\common\RimWorld"

for %%D in (
    "%RIMWORLD_DIR%\Mods\AncientMedievalJapanCore.E2ETarget"
    "%RIMWORLD_DIR%\Mods\AncientMedievalJapanCore.E2E"
    "%RIMWORLD_DIR%\Mods\AncientMedievalJapanCore.MOFixture"
) do (
    if exist "%%~D" (
        rmdir /S /Q "%%~D"
        if errorlevel 1 (
            echo [ERROR] Failed to remove %%~D
            exit /b 1
        )
    )
)

echo [OK] AMJ generated E2E mods removed.
exit /b 0
