# 🏠 Rhokawi Properties - Real Estate Platform

A comprehensive full-stack real estate platform built with **React** frontend and **Flask** backend, featuring property management, user authentication, advanced search, and role-based access control.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Development](#-development)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Technologies](#-technologies)
- [Contributing](#-contributing)

## ✨ Features

### 🏠 **Property Management**
- Complete CRUD operations for properties
- Advanced search with multiple filters (location, price, type, bedrooms)
- Property image galleries with secure uploads
- Agent-specific property management
- Property status tracking (available, sold, pending)

### 🔐 **Authentication & Authorization**
- JWT-based authentication system
- Role-based access control (Admin, Agent, Client)
- Secure password hashing
- Token refresh mechanism

### 👥 **User Roles**
- **Admin**: Full system access, user management, all properties
- **Agent**: Create/manage own properties, view inquiries
- **Client**: Browse properties, save favorites, send inquiries

### 🔍 **Advanced Search**
- Location-based filtering
- Price range search
- Property type filtering
- Bedroom/bathroom filters
- Pagination support

### ❤️ **Favorites System**
- Save properties to favorites
- View saved properties
- Remove from favorites
- User-specific favorites management

### 📧 **Contact System**
- Contact form submissions
- Property-specific inquiries
- Message status management
- Admin message dashboard

### 📁 **File Management**
- Secure image uploads
- Multiple file support
- File type validation
- Size limits and optimization

## 📁 Project Structure

```
rhokawi-properties/
├── backend/                    # Flask API Server
│   ├── app/                   
│   │   ├── routes/            # API route blueprints
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   ├── properties.py # Property management
│   │   │   ├── favorites.py  # User favorites
│   │   │   ├── contact.py    # Contact messages
│   │   │   ├── upload.py     # File uploads
│   │   │   └── users.py      # User management
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Validation schemas
│   │   ├── utils.py          # Utility functions
│   │   └── __init__.py       # App factory
│   ├── instance/             # Database files
│   ├── venv/                 # Python virtual environment
│   ├── run.py               # Application entry point
│   ├── config.py            # Configuration settings
│   ├── init_db.py          # Database initialization
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile            # Deployment config
│   └── render.yaml         # Render deployment
│
├── frontend/                  # React Application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── contexts/        # React contexts
│   │   ├── lib/            # Utilities and API client
│   │   │   └── api.js      # Complete API service layer
│   │   └── main.jsx        # Application entry point
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js      # Vite configuration
│   ├── tailwind.config.js  # Tailwind CSS config
│   └── index.html          # HTML template
│
├── docs/                     # Documentation
│   ├── README.md            # Comprehensive project guide
│   ├── FRONTEND_BACKEND_CONNECTION.md
│   ├── TRANSFORMATION_COMPLETE.md
│   └── FLASK_SETUP_SUMMARY.md
│
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v18+)
- **Python** (v3.9+)
- **Git**

### 1. Clone Repository
```bash
git clone https://github.com/Evian1k/rhokawi2.git
cd rhokawi2
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python run.py
```
**Backend runs on:** http://localhost:5000

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
**Frontend runs on:** http://localhost:3000

### 4. Test the Application
- Visit: http://localhost:3000
- Login credentials:
  - **Admin:** `admin` / `admin123`
  - **Agent:** `agent1` / `agent123`
  - **Client:** `client1` / `client123`

## 🛠️ Development

### Backend Development
```bash
cd backend
source venv/bin/activate
python run.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Database Management
```bash
cd backend
source venv/bin/activate
python init_db.py  # Initialize/reset database
```

## 📚 API Documentation

### Base URL
- **Development:** `http://localhost:5000/api`
- **Production:** `https://your-domain.com/api`

### Authentication Endpoints
```
POST   /auth/login           # User login
POST   /auth/register        # User registration
GET    /auth/me              # Get current user
POST   /auth/refresh         # Refresh token
```

### Property Endpoints
```
GET    /properties           # List properties (paginated)
GET    /properties/search    # Advanced search
GET    /properties/{id}      # Get property details
POST   /properties           # Create property (agent/admin)
PUT    /properties/{id}      # Update property
DELETE /properties/{id}      # Delete property
```

### Additional Endpoints
- **Favorites:** `/favorites`
- **Contact:** `/contact`
- **Upload:** `/upload`
- **Users:** `/users`

See [API Documentation](docs/FRONTEND_BACKEND_CONNECTION.md) for complete details.

## 🚀 Deployment

### Backend Deployment (Render.com)
1. Connect GitHub repository to Render
2. Use `backend/render.yaml` configuration
3. Set environment variables
4. Deploy automatically

### Frontend Deployment (Vercel/Netlify)
1. Connect GitHub repository
2. Set build directory to `frontend`
3. Configure environment variables
4. Deploy

### Environment Variables

**Backend (.env):**
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
CORS_ORIGINS=https://your-frontend-domain.com
```

**Frontend (.env):**
```env
VITE_API_URL=https://your-backend-domain.com/api
```

## 🛠️ Technologies

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **JWT** - Authentication tokens
- **Marshmallow** - Data validation
- **Flask-CORS** - Cross-origin requests
- **Gunicorn** - Production server

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Framer Motion** - Animations
- **Radix UI** - Component library

### Database
- **SQLite** (Development)
- **PostgreSQL** (Production)

## 📊 Features Overview

| Feature | Status | Description |
|---------|--------|-------------|
| 🔐 Authentication | ✅ Complete | JWT-based with role management |
| 🏠 Property Management | ✅ Complete | Full CRUD with search |
| ❤️ Favorites System | ✅ Complete | Save/remove properties |
| 📧 Contact System | ✅ Complete | Message management |
| 📁 File Uploads | ✅ Complete | Image upload system |
| 🔍 Advanced Search | ✅ Complete | Multiple filter options |
| 👥 User Roles | ✅ Complete | Admin/Agent/Client |
| 📱 Responsive Design | ✅ Complete | Mobile-friendly UI |
| 🚀 Production Ready | ✅ Complete | Deployment configured |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:
- 📧 Email: info@rhokawiproperties.com
- 📱 Phone: +254 713 663 866
- 🌐 Website: [Rhokawi Properties](https://rhokawiproperties.com)

---

**Built with ❤️ for modern real estate management**