#!/bin/bash

# Real Estate Flask API Startup Script

echo "🏠 Starting Real Estate Flask API..."

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

# Start the Flask application
echo "🚀 Starting server on http://localhost:5000"
echo "📊 API documentation available in README.md"
echo "👤 Default admin: username=admin, password=admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

python app.py