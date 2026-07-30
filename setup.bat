@echo off
REM TaskFlow - Quick Setup Script for Windows

echo.
echo ====================================
echo   TaskFlow - Team Task Manager
echo   Setup Script (Windows)
echo ====================================
echo.

REM Check Python Installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python is installed

REM Create Virtual Environment
echo.
echo [STEP 1] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate Virtual Environment
echo.
echo [STEP 2] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Install Requirements
echo.
echo [STEP 3] Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Create Uploads Directory
echo.
echo [STEP 4] Creating necessary directories...
if not exist "app\static\uploads" mkdir app\static\uploads
if not exist "logs" mkdir logs
echo [OK] Directories created

REM Display Instructions
echo.
echo ====================================
echo   Setup Complete!
echo ====================================
echo.
echo [IMPORTANT] Before running the application:
echo.
echo 1. Setup MySQL Database:
echo    - Open MySQL Command Line
echo    - Login: mysql -u root -p
echo    - Run: source database.sql
echo.
echo 2. Update Database Configuration:
echo    - Edit .env file
echo    - Update DATABASE_URL with your MySQL credentials
echo    - Default: mysql+pymysql://root:password@localhost:3306/taskflow_db
echo.
echo 3. Run the Application:
echo    - Execute: python app.py
echo    - Open: http://localhost:5000
echo.
echo [LOGIN CREDENTIALS]
echo    Username: admin
echo    Password: password123
echo.
echo ====================================
echo.
pause
