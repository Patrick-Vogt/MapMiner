#!/bin/bash

echo "🚀 Starting Google Maps Scraper Dashboard..."
echo ""

# Check if backend virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    echo "✅ Virtual environment created and dependencies installed"
    echo ""
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Node modules not found. Installing..."
    cd frontend
    npm install
    cd ..
    echo "✅ Node modules installed"
    echo ""
fi

# Start backend in background
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend development server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Application started successfully!"
echo ""
echo "📍 Backend running on: http://localhost:5001"
echo "📍 Frontend running on: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '⏹️  Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
