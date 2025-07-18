# Flask Backend API

Real estate platform backend built with Flask, featuring JWT authentication, property management, and comprehensive API endpoints.

## 🚀 Quick Start

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run development server
python run.py
```

## 🔧 Configuration

### Environment Variables (.env)
```env
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
CORS_ORIGINS=http://localhost:3000,*
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user

### Properties
- `GET /api/properties` - List properties
- `GET /api/properties/search` - Search properties
- `POST /api/properties` - Create property (agent/admin)

### Additional Endpoints
- `/api/favorites` - User favorites
- `/api/contact` - Contact messages
- `/api/upload` - File uploads

## 🔐 Test Credentials

- **Admin:** `admin` / `admin123`
- **Agent:** `agent1` / `agent123`
- **Client:** `client1` / `client123`

## 🚀 Deployment

Use the provided `Procfile` and `render.yaml` for deployment to Render.com or similar platforms.