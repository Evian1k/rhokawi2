#!/usr/bin/env python3
"""
Flask application entry point.
"""

from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # Get environment variables for configuration
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)