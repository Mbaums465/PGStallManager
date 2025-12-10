@echo off
setlocal ENABLEDELAYEDEXPANSION

:: --------------------------------------------
:: CONFIG
:: --------------------------------------------
set PYTHON_EXE=python
set PYTHONW_EXE=pythonw
set SCRIPT_NAME=PGStallManager_prod.py

:: --------------------------------------------
:: CHECK PYTHON
:: --------------------------------------------
where %PYTHON_EXE% >nul 2>&1
if errorlevel 1 (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Python is not installed or not in PATH. Please install Python 3.10+ from python.org','Missing Python')"
    exit /b
)

:: --------------------------------------------
:: CHECK pythonw
:: --------------------------------------------
where %PYTHONW_EXE% >nul 2>&1
if errorlevel 1 (
    powershell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('pythonw.exe not found. Your Python install may be broken.','Missing pythonw')"
    exit /b
)

:: --------------------------------------------
:: UPGRADE PIP SILENTLY
:: --------------------------------------------
%PYTHON_EXE% -m pip install --upgrade pip --quiet --disable-pip-version-check >nul 2>&1

:: --------------------------------------------
:: OPTIONAL PACKAGE CHECK TEMPLATE
:: (Nothing required for your current script)
:: --------------------------------------------
:: Example for future:
:: %PYTHON_EXE% -c "import requests" >nul 2>&1 || %PYTHON_EXE% -m pip install requests --quiet

:: --------------------------------------------
:: RUN GUI SILENTLY (NO CMD WINDOW)
:: --------------------------------------------
start "" %PYTHONW_EXE% "%~dp0%SCRIPT_NAME%"

exit
