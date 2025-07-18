# Flask Backend API

A well-structured Flask backend with authentication, CORS support, and environment variable configuration.

## Project Structure

```
├── run.py                 # Application entry point
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables example
├── app/
│   ├── __init__.py      # App factory
│   ├── models.py        # Database models
│   ├── schemas.py       # Marshmallow schemas
│   ├── utils.py         # Utility functions
│   └── routes/
│       ├── __init__.py  # Routes registration
│       ├── main.py      # Main routes
│       ├── auth.py      # Authentication routes
│       ├── users.py     # User management routes
│       └── posts.py     # Post management routes
```

## Features

- **Flask Application Factory**: Modular app creation with configuration support
- **CORS Enabled**: Cross-origin resource sharing configured
- **Environment Variables**: Configuration through environment variables
- **JWT Authentication**: Secure authentication with access and refresh tokens
- **Database Integration**: SQLAlchemy ORM with SQLite (configurable)
- **Input Validation**: Marshmallow schemas for request/response validation
- **Error Handling**: Standardized error responses
- **Pagination**: Built-in pagination for list endpoints
- **Admin System**: Role-based access control

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///app.db
CORS_ORIGINS=http://localhost:3000,*
```

### 3. Initialize Database

```bash
python run.py
```

The database will be automatically created when you first run the application.

### 4. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api` - API information

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Users
- `GET /api/users` - Get all users (paginated)
- `GET /api/users/<id>` - Get specific user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user (admin only)
- `GET /api/users/search?q=<query>` - Search users

### Posts
- `GET /api/posts` - Get all posts (paginated)
- `GET /api/posts/<id>` - Get specific post
- `POST /api/posts` - Create new post (authenticated)
- `PUT /api/posts/<id>` - Update post (owner/admin)
- `DELETE /api/posts/<id>` - Delete post (owner/admin)
- `GET /api/posts/search?q=<query>` - Search posts
- `GET /api/posts/user/<user_id>` - Get posts by user

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Registration Example

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login Example

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword"
  }'
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | development |
| `FLASK_DEBUG` | Enable debug mode | False |
| `FLASK_HOST` | Host to bind to | 0.0.0.0 |
| `FLASK_PORT` | Port to listen on | 5000 |
| `SECRET_KEY` | Flask secret key | dev-secret-key |
| `JWT_SECRET_KEY` | JWT signing key | Uses SECRET_KEY |
| `DATABASE_URL` | Database connection URL | sqlite:///app.db |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | * |
| `REDIS_URL` | Redis URL for rate limiting | memory:// |

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `first_name`: Optional first name
- `last_name`: Optional last name
- `is_active`: Account status
- `is_admin`: Admin privileges
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Post
- `id`: Primary key
- `title`: Post title
- `content`: Post content
- `author_id`: Foreign key to User
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Error Handling

All errors return a standardized JSON format:

```json
{
  "error": "Error Type",
  "message": "Human-readable error message",
  "status_code": 400
}
```

## Development

### Adding New Routes

1. Create a new blueprint in `app/routes/`
2. Register it in `app/routes/__init__.py`
3. Add any new models to `app/models.py`
4. Create corresponding schemas in `app/schemas.py`

### Database Migrations

For production use, consider adding Flask-Migrate:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Production Deployment

1. Set `FLASK_ENV=production`
2. Use a production database (PostgreSQL recommended)
3. Set strong `SECRET_KEY` and `JWT_SECRET_KEY`
4. Configure proper CORS origins
5. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```