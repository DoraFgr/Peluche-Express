@echo off
echo Building Peluche Express .exe...
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build the executable
echo Building executable with PyInstaller...
pyinstaller peluche_express.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================
    echo Build completed successfully!
    echo.
    echo Your game executable is located at:
    echo dist\PelucheExpress.exe
    echo.
    echo You can now share this file with your brother!
    echo ================================
) else (
    echo.
    echo Build failed! Check the output above for errors.
)

pause
