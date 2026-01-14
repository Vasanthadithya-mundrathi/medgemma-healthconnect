@echo off
REM Quick Start Script for MedGemma HealthConnect (Windows)

echo ===============================================================
echo.
echo         MedGemma HealthConnect Quick Start
echo         Privacy-First Healthcare AI
echo.
echo ===============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INFO] Installing dependencies...
    echo This may take a few minutes...
    pip install -r requirements.txt
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

REM Create .env if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env configuration...
    copy .env.example .env
    echo [OK] Configuration file created
)

REM Run tests
echo.
echo Running system tests...
python tests\test_structure.py
if errorlevel 1 (
    echo [ERROR] Some tests failed
    pause
    exit /b 1
)
echo [OK] All tests passed

REM Display information
echo.
echo ===============================================================
echo                   Ready to Launch!
echo ===============================================================
echo.
echo Starting MedGemma HealthConnect...
echo.
echo The application will open in your browser at:
echo http://localhost:8501
echo.
echo To stop the application, press Ctrl+C
echo.
echo [WARNING] First run will download AI models (~2-4GB)
echo           This is a one-time download.
echo.

REM Start Streamlit
streamlit run app.py
