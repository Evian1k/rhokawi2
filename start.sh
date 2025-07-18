#!/bin/bash

# Rhokawi Properties Development Launcher
echo "🏠 Starting Rhokawi Properties Platform..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal trap
trap cleanup SIGINT SIGTERM

# Start Backend
echo "🚀 Starting Flask Backend..."
cd backend
source venv/bin/activate
python run.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start Frontend
echo "🚀 Starting React Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both servers are starting..."
echo "🔗 Backend:  http://localhost:5000"
echo "🔗 Frontend: http://localhost:3000"
echo ""
echo "📝 Logs will appear below..."
echo "🛑 Press Ctrl+C to stop both servers"
echo ""

# Wait for processes to finish
wait $BACKEND_PID $FRONTEND_PID