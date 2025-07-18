# Real Estate Platform API

A comprehensive Flask backend API for real estate platform with property management, user authentication, role-based access control, and file uploads.

## 🏗️ Project Structure

```
├── run.py                 # Application entry point
├── init_db.py            # Database initialization script
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── render.yaml          # Render deployment config
├── .env                 # Environment variables (development)
├── .env.example         # Environment variables template
└── app/
    ├── __init__.py      # Flask app factory
    ├── models.py        # Database models
    ├── schemas.py       # Validation schemas
    ├── utils.py         # Utility functions
    └── routes/
        ├── __init__.py  # Routes registration
        ├── main.py      # Health check endpoints
        ├── auth.py      # Authentication routes
        ├── users.py     # User management routes
        ├── properties.py # Property management routes
        ├── favorites.py  # User favorites routes
        ├── contact.py    # Contact message routes
        └── upload.py     # File upload routes
```

## ✨ Features

### 🔐 **Authentication & Authorization**
- JWT authentication with access and refresh tokens
- Role-based access control (Admin, Agent, Client)
- Password hashing with Werkzeug
- Protected routes with decorators

### 🏠 **Property Management**
- CRUD operations for properties
- Advanced search with multiple filters
- Property image management
- Agent-specific property listings
- Property status management (available, sold, pending)

### ❤️ **User Favorites**
- Save/remove properties to favorites
- View user's favorite properties
- Check favorite status for properties

### 📧 **Contact System**
- Contact form submissions
- Property-specific inquiries
- Message status management (unread, read, replied)
- Admin message management

### 📁 **File Upload System**
- Secure image uploads
- Multiple file upload support
- File type validation (PNG, JPG, JPEG, GIF, WEBP)
- File size limits (16MB per file, 100MB total)
- Automatic file serving

### 🔍 **Advanced Search**
- Location-based search
- Price range filtering
- Property type filtering
- Bedroom count filtering
- Pagination support

## 🚀 API Endpoints

### **Authentication**
```
POST   /api/auth/register     - Register new user
POST   /api/auth/login        - User login
POST   /api/auth/refresh      - Refresh access token
GET    /api/auth/me           - Get current user info
```

### **Properties**
```
GET    /api/properties        - Get all properties (paginated)
GET    /api/properties/search - Search properties with filters
GET    /api/properties/{id}   - Get specific property
POST   /api/properties        - Create property (agent/admin)
PUT    /api/properties/{id}   - Update property (owner/admin)
DELETE /api/properties/{id}   - Delete property (owner/admin)
GET    /api/properties/agent/{id} - Get properties by agent
POST   /api/properties/{id}/images - Add images to property
```

### **Favorites**
```
GET    /api/favorites         - Get user's favorite properties
POST   /api/favorites         - Add property to favorites
DELETE /api/favorites/{id}    - Remove property from favorites
GET    /api/favorites/{id}/check - Check if property is favorited
```

### **Contact Messages**
```
POST   /api/contact           - Send contact message (public)
GET    /api/contact           - Get all messages (admin)
GET    /api/contact/{id}      - Get specific message (admin)
PUT    /api/contact/{id}/status - Update message status (admin)
DELETE /api/contact/{id}      - Delete message (admin)
GET    /api/contact/my-messages - Get user's messages
```

### **File Upload**
```
POST   /api/upload            - Upload single file
POST   /api/upload/multiple   - Upload multiple files
GET    /api/upload/{filename} - Serve uploaded file
```

### **Users**
```
GET    /api/users             - Get all users (paginated)
GET    /api/users/{id}        - Get specific user
PUT    /api/users/{id}        - Update user (self/admin)
DELETE /api/users/{id}        - Delete user (admin)
GET    /api/users/search      - Search users
```

## 👥 User Roles

### **Client** (Default)
- View properties
- Search and filter properties
- Save/remove favorites
- Send contact messages
- View own profile and messages

### **Agent**
- All client permissions
- Create, update, delete own properties
- Manage property images
- View all contact messages for their properties

### **Admin**
- All permissions
- Manage all users and properties
- View and manage all contact messages
- Delete any content
- Access admin-only endpoints

## 📊 Database Models

### **User**
- Basic user information (username, email, name)
- Role-based permissions
- Password hashing
- Timestamps

### **Property**
- Complete property details
- JSON fields for features and images
- Agent relationship
- Status management
- Advanced search fields

### **ContactMessage**
- Contact form submissions
- Property-specific inquiries
- Status tracking
- User relationship (optional)

### **User Favorites** (Many-to-Many)
- User ↔ Property relationship table
- Efficient favorite management

## 🛠️ Installation & Setup

### 1. **Clone Repository**
```bash
git clone <repository-url>
cd real-estate-api
```

### 2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. **Initialize Database**
```bash
python init_db.py
```

### 6. **Run Application**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 🔧 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment mode | development | No |
| `FLASK_DEBUG` | Debug mode | False | No |
| `FLASK_HOST` | Host to bind | 0.0.0.0 | No |
| `FLASK_PORT` | Port to listen | 5000 | No |
| `SECRET_KEY` | Flask secret key | - | Yes |
| `JWT_SECRET_KEY` | JWT signing key | Uses SECRET_KEY | No |
| `DATABASE_URL` | Database connection | sqlite:///app.db | No |
| `CORS_ORIGINS` | Allowed CORS origins | * | No |

## 🧪 Sample Data

The `init_db.py` script creates sample users and properties:

**Sample Users:**
- **Admin:** `admin` / `admin123`
- **Agent:** `agent1` / `agent123`
- **Client:** `client1` / `client123`

**Sample Properties:**
- Beautiful Family Home (Los Angeles)
- Downtown Luxury Apartment (New York)
- Cozy Townhouse (Austin)

## 🔍 Search Examples

### **Basic Property Search**
```bash
GET /api/properties/search?location=Los Angeles&min_price=500000&max_price=1000000
```

### **Advanced Filtering**
```bash
GET /api/properties/search?property_type=house&bedrooms=3&location=CA&page=1&per_page=20
```

## 📝 Usage Examples

### **Register New Agent**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "neweagent",
    "email": "newagent@example.com",
    "password": "password123",
    "role": "agent",
    "first_name": "New",
    "last_name": "Agent"
  }'
```

### **Create Property** (Agent/Admin only)
```bash
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "Modern Condo",
    "description": "Beautiful modern condo with city views",
    "property_type": "condo",
    "location": "San Francisco, CA",
    "price": 850000,
    "bedrooms": 2,
    "bathrooms": 2,
    "square_feet": 1200,
    "features": ["Balcony", "Modern Kitchen", "Parking"]
  }'
```

### **Add to Favorites**
```bash
curl -X POST http://localhost:5000/api/favorites \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"property_id": 1}'
```

### **Upload Property Image**
```bash
curl -X POST http://localhost:5000/api/upload \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@image.jpg"
```

## 🚀 Deployment

### **Render.com**
1. Connect your GitHub repository to Render
2. Use the provided `render.yaml` configuration
3. Set environment variables in Render dashboard
4. Deploy automatically

### **Manual Deployment**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url

# Initialize database
python init_db.py

# Run with Gunicorn
gunicorn run:app
```

## 🛡️ Security Features

- **JWT Authentication:** Secure token-based authentication
- **Password Hashing:** Werkzeug secure password hashing
- **Role-based Access:** Granular permission system
- **Input Validation:** Marshmallow schema validation
- **File Upload Security:** Type and size validation
- **CORS Configuration:** Configurable cross-origin policies
- **SQL Injection Protection:** SQLAlchemy ORM protection

## 📈 Performance Features

- **Pagination:** Efficient data loading
- **Database Indexing:** Optimized queries
- **File Compression:** Pillow image optimization
- **Lazy Loading:** Efficient relationship loading
- **Query Optimization:** Advanced search queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Open an issue on GitHub
- Check the API documentation at `/api`
- Review the comprehensive error messages