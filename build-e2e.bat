@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "RIMWORLD_DIR=%~1"
if not defined RIMWORLD_DIR set "RIMWORLD_DIR=D:\SteamLibrary\steamapps\common\RimWorld"

set "ROOT=%~dp0"
set "TARGET_MOD_DIR=%RIMWORLD_DIR%\Mods\AncientMedievalJapanCore.E2ETarget"
set "E2E_MOD_DIR=%RIMWORLD_DIR%\Mods\AncientMedievalJapanCore.E2E"
set "MO_FIXTURE_DIR=%RIMWORLD_DIR%\Mods\AncientMedievalJapanCore.MOFixture"
set "CCTO_FIXTURE_DIR=%RIMWORLD_DIR%\Mods\AncientMedievalJapanCore.CCTOFixture"

set "CSC=%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist "%CSC%" set "CSC=%WINDIR%\Microsoft.NET\Framework\v4.0.30319\csc.exe"
if not exist "%CSC%" (
    echo [ERROR] C# compiler was not found.
    exit /b 1
)

set "MANAGED=%RIMWORLD_DIR%\RimWorldWin64_Data\Managed"
set "ASSEMBLY_CSHARP=%MANAGED%\Assembly-CSharp.dll"
set "UNITY_CORE=%MANAGED%\UnityEngine.CoreModule.dll"
set "UNITY_MATH=%MANAGED%\Unity.Mathematics.dll"
set "NETSTANDARD=%MANAGED%\netstandard.dll"
set "STEAMAPPS=%RIMWORLD_DIR%\..\.."

for %%F in ("%ASSEMBLY_CSHARP%" "%UNITY_MATH%" "%NETSTANDARD%") do (
    if not exist "%%~F" (
        echo [ERROR] Required RimWorld managed assembly was not found:
        echo         %%~F
        exit /b 1
    )
)

set "PICKLE_ROOT=%STEAMAPPS%\workshop\content\294100\3791648678"
set "QUICKSTARTS_ROOT=%STEAMAPPS%\workshop\content\294100\3793646067"

set "PICKLE_DLL="
if exist "%PICKLE_ROOT%\1.6\Assemblies\RimWorks.Pickle.dll" set "PICKLE_DLL=%PICKLE_ROOT%\1.6\Assemblies\RimWorks.Pickle.dll"
if not defined PICKLE_DLL if exist "%PICKLE_ROOT%" (
    for /r "%PICKLE_ROOT%" %%F in (RimWorks.Pickle.dll) do (
        if not defined PICKLE_DLL set "PICKLE_DLL=%%~fF"
    )
)

set "QUICKSTARTS_DLL="
if exist "%QUICKSTARTS_ROOT%\1.6\Assemblies\Quickstarts.dll" set "QUICKSTARTS_DLL=%QUICKSTARTS_ROOT%\1.6\Assemblies\Quickstarts.dll"
if not defined QUICKSTARTS_DLL if exist "%QUICKSTARTS_ROOT%" (
    for /r "%QUICKSTARTS_ROOT%" %%F in (Quickstarts.dll) do (
        if not defined QUICKSTARTS_DLL set "QUICKSTARTS_DLL=%%~fF"
    )
)

if not defined PICKLE_DLL (
    echo.
    echo [ERROR] RimWorks.Pickle.dll was not found under:
    echo         %PICKLE_ROOT%
    echo Install/subscribe to Pickle ^(Steam Workshop 3791648678^) first.
    exit /b 1
)

if not defined QUICKSTARTS_DLL (
    echo.
    echo [ERROR] Quickstarts.dll was not found under:
    echo         %QUICKSTARTS_ROOT%
    echo Install/subscribe to Quickstarts ^(Steam Workshop 3793646067^) first.
    exit /b 1
)

echo [1/5] Resetting generated AMJ E2E mods...
for %%D in ("%TARGET_MOD_DIR%" "%E2E_MOD_DIR%" "%MO_FIXTURE_DIR%" "%CCTO_FIXTURE_DIR%") do (
    if exist "%%~D" rmdir /S /Q "%%~D"
)
if errorlevel 1 exit /b 1

mkdir "%TARGET_MOD_DIR%\About" >nul
mkdir "%E2E_MOD_DIR%\About" >nul
mkdir "%E2E_MOD_DIR%\Assemblies" >nul
mkdir "%E2E_MOD_DIR%\Pickle\Assemblies" >nul
mkdir "%E2E_MOD_DIR%\Pickle\Features" >nul
mkdir "%MO_FIXTURE_DIR%\About" >nul
mkdir "%MO_FIXTURE_DIR%\Defs" >nul
mkdir "%CCTO_FIXTURE_DIR%\About" >nul
mkdir "%CCTO_FIXTURE_DIR%\Assemblies" >nul

echo [2/5] Staging AMJ runtime XML and lightweight Medieval Overhaul fixture...
copy /Y "%ROOT%Tests\E2E\TargetMod\About\About.xml" "%TARGET_MOD_DIR%\About\About.xml" >nul
if errorlevel 1 exit /b 1

xcopy "%ROOT%Defs" "%TARGET_MOD_DIR%\Defs" /E /I /Y >nul
if errorlevel 1 exit /b 1

if exist "%ROOT%Languages" (
    xcopy "%ROOT%Languages" "%TARGET_MOD_DIR%\Languages" /E /I /Y >nul
    if errorlevel 1 exit /b 1
)

if exist "%ROOT%Patches" (
    xcopy "%ROOT%Patches" "%TARGET_MOD_DIR%\Patches" /E /I /Y >nul
    if errorlevel 1 exit /b 1
)

copy /Y "%ROOT%Tests\E2E\MOFixture\About\About.xml" "%MO_FIXTURE_DIR%\About\About.xml" >nul
if errorlevel 1 exit /b 1
copy /Y "%ROOT%Tests\E2E\MOFixture\Defs\AMJ_MO_Prereqs.xml" "%MO_FIXTURE_DIR%\Defs\AMJ_MO_Prereqs.xml" >nul
if errorlevel 1 exit /b 1

copy /Y "%ROOT%Tests\E2E\CCTOFixture\About\About.xml" "%CCTO_FIXTURE_DIR%\About\About.xml" >nul
if errorlevel 1 exit /b 1

copy /Y "%ROOT%Tests\E2E\TestMod\About\About.xml" "%E2E_MOD_DIR%\About\About.xml" >nul
if errorlevel 1 exit /b 1
copy /Y "%ROOT%Tests\E2E\TestMod\Pickle\Features\*.feature" "%E2E_MOD_DIR%\Pickle\Features\" >nul
if errorlevel 1 exit /b 1

set "CCTO_FIXTURE_OUTPUT=%CCTO_FIXTURE_DIR%\Assemblies\CropColdToleranceOverhaul.dll"
set "QUICKSTART_OUTPUT=%E2E_MOD_DIR%\Assemblies\AncientMedievalJapanCore.E2E.dll"
set "STEPS_OUTPUT=%E2E_MOD_DIR%\Pickle\Assemblies\AncientMedievalJapanCore.E2E.Steps.dll"

echo [3/6] Building CCTO XML API fixture...
"%CSC%" /nologo /target:library /optimize+ /out:"%CCTO_FIXTURE_OUTPUT%" ^
    /reference:"%ASSEMBLY_CSHARP%" ^
    /reference:"%NETSTANDARD%" ^
    "%ROOT%Tests\E2E\CCTOFixture\ColdToleranceExtension.cs"
if errorlevel 1 exit /b 1

echo [4/6] Building deterministic Quickstarts fixture...
if exist "%UNITY_CORE%" (
    "%CSC%" /nologo /target:library /optimize+ /out:"%QUICKSTART_OUTPUT%" ^
        /reference:"%ASSEMBLY_CSHARP%" ^
        /reference:"%UNITY_CORE%" ^
        /reference:"%UNITY_MATH%" ^
        /reference:"%NETSTANDARD%" ^
        /reference:"%QUICKSTARTS_DLL%" ^
        "%ROOT%Tests\E2E\AmjStageAQuickstart.cs"
) else (
    "%CSC%" /nologo /target:library /optimize+ /out:"%QUICKSTART_OUTPUT%" ^
        /reference:"%ASSEMBLY_CSHARP%" ^
        /reference:"%UNITY_MATH%" ^
        /reference:"%NETSTANDARD%" ^
        /reference:"%QUICKSTARTS_DLL%" ^
        "%ROOT%Tests\E2E\AmjStageAQuickstart.cs"
)
if errorlevel 1 exit /b 1

echo [5/6] Building Pickle step assembly...
if exist "%UNITY_CORE%" (
    "%CSC%" /nologo /target:library /optimize+ /out:"%STEPS_OUTPUT%" ^
        /reference:"%ASSEMBLY_CSHARP%" ^
        /reference:"%UNITY_CORE%" ^
        /reference:"%UNITY_MATH%" ^
        /reference:"%NETSTANDARD%" ^
        /reference:"%PICKLE_DLL%" ^
        "%ROOT%Tests\E2E\StageASteps.cs"
) else (
    "%CSC%" /nologo /target:library /optimize+ /out:"%STEPS_OUTPUT%" ^
        /reference:"%ASSEMBLY_CSHARP%" ^
        /reference:"%UNITY_MATH%" ^
        /reference:"%NETSTANDARD%" ^
        /reference:"%PICKLE_DLL%" ^
        "%ROOT%Tests\E2E\StageASteps.cs"
)
if errorlevel 1 exit /b 1

echo [6/6] Verifying generated E2E layout...
if not exist "%CCTO_FIXTURE_OUTPUT%" exit /b 1
if not exist "%QUICKSTART_OUTPUT%" exit /b 1
if not exist "%STEPS_OUTPUT%" exit /b 1
if not exist "%E2E_MOD_DIR%\Pickle\Features\stage-a.feature" exit /b 1
if not exist "%TARGET_MOD_DIR%\Defs\RecipeDefs\Recipes_GrainProcessing.xml" exit /b 1
if not exist "%MO_FIXTURE_DIR%\Defs\AMJ_MO_Prereqs.xml" exit /b 1

echo.
echo [OK] AMJ E2E test mods are ready:
echo      %TARGET_MOD_DIR%
echo      %E2E_MOD_DIR%
echo      %MO_FIXTURE_DIR%
echo      %CCTO_FIXTURE_DIR%
exit /b 0
