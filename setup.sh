#!/bin/bash

# Rhokawi Properties Setup Script
echo "🏠 Setting up Rhokawi Properties Platform..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo "🔧 Setting up Flask Backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

echo "✅ Backend setup complete"

# Setup Frontend
echo "🔧 Setting up React Frontend..."
cd ../frontend

# Install Node.js dependencies
npm install

echo "✅ Frontend setup complete"

# Return to root directory
cd ..

echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Start backend:  cd backend && source venv/bin/activate && python run.py"
echo "2. Start frontend: cd frontend && npm run dev"
echo "3. Visit: http://localhost:3000"
echo ""
echo "🔐 Test credentials:"
echo "   Admin: admin / admin123"
echo "   Agent: agent1 / agent123"
echo "   Client: client1 / client123"