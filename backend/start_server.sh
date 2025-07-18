#!/bin/bash
# Flask API Server Startup Script
# This script starts the Flask server with all fixes applied

echo "=== RHOKAWI FLASK API SERVER ==="
echo "Starting server with all fixes applied..."

# Activate virtual environment
source venv/bin/activate

# Check if database needs initialization
python -c "
from app import create_app, db
from app.models import Property, User
app = create_app()
with app.app_context():
    try:
        # Test database connection
        Property.query.first()
        User.query.first()
        print('✓ Database is ready')
    except Exception as e:
        print('Database needs initialization, running fixes...')
        exec(open('fix_database_issues.py').read())
"

echo "Starting Flask server..."
echo "Server will be available at: http://127.0.0.1:5000"
echo "API base URL: http://127.0.0.1:5000/api"
echo ""
echo "Test endpoints:"
echo "  GET  /api/properties    - List all properties"
echo "  GET  /api/properties/2  - Get specific property"
echo "  POST /api/auth/login    - Login (admin/admin123)"
echo "  GET  /api/contact       - Contact messages (auth required)"
echo "  POST /api/upload        - Upload files (auth required)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python run.py
