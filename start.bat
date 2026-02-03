@echo off
echo Starting Google Maps Scraper Dashboard...
echo.

REM Check if backend virtual environment exists
if not exist "backend\venv" (
    echo Virtual environment not found. Creating one...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
    echo Virtual environment created and dependencies installed
    echo.
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo Node modules not found. Installing...
    cd frontend
    call npm install
    cd ..
    echo Node modules installed
    echo.
)

REM Start backend
echo Starting backend server...
cd backend
call venv\Scripts\activate
start /B python app.py
cd ..

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting frontend development server...
cd frontend
start /B npm run dev
cd ..

echo.
echo Application started successfully!
echo.
echo Backend running on: http://localhost:5001
echo Frontend running on: http://localhost:5173
echo.
echo Press Ctrl+C to stop
echo.

pause
