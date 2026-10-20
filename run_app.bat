@echo off
title SpamShield AI - Flask Web Application
echo =====================================================================
echo  SpamShield AI - Smart Messages. Safer Digital Life. (Flask Edition)
echo =====================================================================
echo.
echo Starting SpamShield AI local web server on http://127.0.0.1:5000...
echo.

:: 1. Check direct installed Python 3.11 path first
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" app.py
    goto end
)

:: 2. Try py launcher
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py app.py
    goto end
)

:: 3. Test if system python runs
python -c "exit(0)" >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python app.py
    goto end
)

echo [ERROR] Python was not found. Please ensure Python 3.10+ is installed.
pause

:end
