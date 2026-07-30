#!/bin/bash

# TaskFlow - Quick Setup Script for Linux/macOS

echo ""
echo "===================================="
echo "  TaskFlow - Team Task Manager"
echo "  Setup Script (Linux/macOS)"
echo "===================================="
echo ""

# Check Python Installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[OK] Python 3 is installed"
python3 --version

# Create Virtual Environment
echo ""
echo "[STEP 1] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

# Activate Virtual Environment
echo ""
echo "[STEP 2] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi
echo "[OK] Virtual environment activated"

# Install Requirements
echo ""
echo "[STEP 3] Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
echo "[OK] Dependencies installed"

# Create Necessary Directories
echo ""
echo "[STEP 4] Creating necessary directories..."
mkdir -p app/static/uploads
mkdir -p logs
echo "[OK] Directories created"

# Display Instructions
echo ""
echo "===================================="
echo "  Setup Complete!"
echo "===================================="
echo ""
echo "[IMPORTANT] Before running the application:"
echo ""
echo "1. Setup MySQL Database:"
echo "   - Open MySQL Command Line"
echo "   - Login: mysql -u root -p"
echo "   - Run: source database.sql"
echo ""
echo "2. Update Database Configuration:"
echo "   - Edit .env file"
echo "   - Update DATABASE_URL with your MySQL credentials"
echo "   - Default: mysql+pymysql://root:password@localhost:3306/taskflow_db"
echo ""
echo "3. Run the Application:"
echo "   - Execute: python app.py"
echo "   - Open: http://localhost:5000"
echo ""
echo "[LOGIN CREDENTIALS]"
echo "   Username: admin"
echo "   Password: password123"
echo ""
echo "===================================="
echo ""
