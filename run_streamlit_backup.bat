@echo off
title SpamShield AI - Streamlit Backup Launcher
echo =====================================================================
echo  SpamShield AI - Original Streamlit App (Backup)
echo =====================================================================
echo.
echo Starting backup Streamlit application...
echo.

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" -m streamlit run app_streamlit_backup.py
    goto end
)

streamlit run app_streamlit_backup.py

:end
