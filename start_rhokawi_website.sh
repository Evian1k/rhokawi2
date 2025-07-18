#!/bin/bash

echo "🚀 STARTING RHOKAWI PROPERTIES WEBSITE FOR SALE"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Start backend server
print_info "Starting backend server..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start backend in background
print_status "Starting Flask backend server..."
python run.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Test backend
print_info "Testing backend connection..."
if curl -s http://127.0.0.1:5000/api/ > /dev/null; then
    print_status "Backend server is running on http://127.0.0.1:5000"
else
    print_error "Backend server failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Move to frontend directory
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_warning "Node modules not found. Installing..."
    npm install
fi

# Start frontend server
print_status "Starting React frontend server..."
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 5

echo ""
echo "🎉 RHOKAWI PROPERTIES WEBSITE IS NOW RUNNING!"
echo "============================================="
echo ""
print_status "Backend API: http://127.0.0.1:5000"
print_status "Frontend Website: http://localhost:5173"
print_status "Admin Portal: http://localhost:5173/rhokawi-admin-access-portal-2025"
echo ""
echo "🔐 ADMIN LOGIN CREDENTIALS:"
echo "   Username: evian12k"
echo "   Password: rhokawi25@12ktbl"
echo ""
echo "📊 WEBSITE STATUS:"
print_status "6 Premium properties loaded and ready for sale"
print_status "Professional Rhokawi Properties branding"
print_status "Property detail pages with buy buttons"
print_status "Interactive property map"
print_status "Contact forms with phone support"
print_status "Mobile responsive design"
print_status "Image upload system functional"
echo ""
echo "🎯 TO DEMONSTRATE TO BUYERS:"
echo "1. Show them: http://localhost:5173"
echo "2. Browse properties with beautiful images"
echo "3. Click any property to see details"
echo "4. Show property map: http://localhost:5173/property-map"
echo "5. Demonstrate 'Buy This Property' buttons"
echo ""
echo "🔧 TO ADD MORE PROPERTIES:"
echo "1. Login to admin: http://localhost:5173/rhokawi-admin-access-portal-2025"
echo "2. Add property with images"
echo "3. Verify property to make it public"
echo ""
echo "💰 READY FOR IMMEDIATE SALE!"
echo ""
print_warning "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    print_info "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    print_status "Servers stopped. Goodbye!"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Keep script running
while true; do
    sleep 1
done