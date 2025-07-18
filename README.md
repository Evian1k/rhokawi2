# Real Estate Flask API

A comprehensive Flask backend for a real estate application with authentication, role-based access control, property management, favorites, and contact functionality.

## Features

- 🔐 User authentication (register, login, logout)
- 👥 Role-based access control (admin, agent, client)
- 🏠 Complete property CRUD operations
- 🔍 Property search and filtering
- 📄 Pagination for all listing endpoints
- ❤️ Favorite properties functionality
- 📧 Contact inquiry system
- 📁 Image upload with file serving
- 🔒 Secure password hashing
- 📊 JSON API responses

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Database

The application uses SQLite by default. The database file `real_estate.db` will be created automatically on first run.

### Default Admin User
- Username: `admin`
- Password: `admin123`
- Role: `admin`

## API Endpoints

### Authentication

#### Register User
- **POST** `/api/register`
- **Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "client"
}
```
- **Response:** User object with success message

#### Login
- **POST** `/api/login`
- **Body:**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```
- **Response:** User object with success message

#### Logout
- **POST** `/api/logout`
- **Auth:** Required
- **Response:** Success message

#### Get Current User
- **GET** `/api/me`
- **Auth:** Required
- **Response:** Current user information

### Properties

#### Get Properties (with search and pagination)
- **GET** `/api/properties`
- **Query Parameters:**
  - `page` (default: 1)
  - `per_page` (default: 10)
  - `location` (string, partial match)
  - `min_price` (float)
  - `max_price` (float)
  - `bedrooms` (integer)
- **Response:** Paginated list of properties

#### Get Single Property
- **GET** `/api/properties/{id}`
- **Response:** Property details

#### Create Property
- **POST** `/api/properties`
- **Auth:** Required (admin/agent only)
- **Body:**
```json
{
  "title": "Beautiful House",
  "description": "A lovely 3-bedroom house...",
  "image_url": "/uploads/image.jpg",
  "location": "123 Main St, City",
  "type": "house",
  "price": 450000,
  "bedrooms": 3,
  "bathrooms": 2,
  "square_feet": 2000
}
```

#### Update Property
- **PUT** `/api/properties/{id}`
- **Auth:** Required (admin/agent, owner only)
- **Body:** Same as create (partial updates allowed)

#### Delete Property
- **DELETE** `/api/properties/{id}`
- **Auth:** Required (admin/agent, owner only)

### File Upload

#### Upload Image
- **POST** `/api/upload`
- **Auth:** Required
- **Body:** `multipart/form-data` with `file` field
- **Supported formats:** PNG, JPG, JPEG, GIF
- **Response:**
```json
{
  "message": "File uploaded successfully",
  "url": "/uploads/unique-filename.jpg"
}
```

### Favorites

#### Get User's Favorites
- **GET** `/api/favorites`
- **Auth:** Required
- **Query Parameters:** `page`, `per_page`
- **Response:** Paginated list of favorited properties

#### Add to Favorites
- **POST** `/api/favorites/{property_id}`
- **Auth:** Required
- **Response:** Success message

#### Remove from Favorites
- **DELETE** `/api/favorites/{property_id}`
- **Auth:** Required
- **Response:** Success message

### Contact

#### Submit Contact Inquiry
- **POST** `/api/contact`
- **Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-0123",
  "message": "I'm interested in this property...",
  "property_id": 1
}
```

#### Get Contact Inquiries
- **GET** `/api/contacts`
- **Auth:** Required (admin/agent only)
- **Query Parameters:** `page`, `per_page`
- **Response:** Paginated list of contact inquiries

## User Roles

### Client
- View properties
- Search and filter properties
- Add/remove favorites
- Submit contact inquiries
- Upload images

### Agent
- All client permissions
- Create properties
- Update/delete own properties
- View contact inquiries

### Admin
- All agent permissions
- Update/delete any properties
- Create admin/agent accounts
- Full system access

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `role`: User role (admin/agent/client)
- `created_at`: Account creation timestamp

### Property
- `id`: Primary key
- `title`: Property title
- `description`: Detailed description
- `image_url`: Property image URL
- `location`: Property address/location
- `type`: Property type (house/apartment/condo/etc.)
- `price`: Property price
- `bedrooms`: Number of bedrooms
- `bathrooms`: Number of bathrooms
- `square_feet`: Property size in square feet
- `owner_id`: Foreign key to User
- `created_at`/`updated_at`: Timestamps

### Favorite
- `id`: Primary key
- `user_id`: Foreign key to User
- `property_id`: Foreign key to Property
- `created_at`: Timestamp

### Contact
- `id`: Primary key
- `name`: Contact name
- `email`: Contact email
- `phone`: Contact phone (optional)
- `message`: Inquiry message
- `property_id`: Related property (optional)
- `user_id`: Submitting user (optional)
- `created_at`: Timestamp

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

Error responses include a JSON object with an `error` field describing the issue.

## Security Features

- Session-based authentication
- Password hashing with bcrypt
- Role-based access control
- Input validation
- File upload restrictions
- SQL injection protection (SQLAlchemy ORM)

## Example Usage

### Complete workflow example:

1. **Register a new agent:**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "email": "agent@example.com", "password": "password123"}'
```

2. **Login:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "password": "password123"}' \
  -c cookies.txt
```

3. **Upload an image:**
```bash
curl -X POST http://localhost:5000/api/upload \
  -b cookies.txt \
  -F "file=@house.jpg"
```

4. **Create a property:**
```bash
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Modern Family Home",
    "description": "Beautiful 4-bedroom house in quiet neighborhood",
    "image_url": "/uploads/house.jpg",
    "location": "123 Oak Street, Springfield",
    "type": "house",
    "price": 425000,
    "bedrooms": 4,
    "bathrooms": 3,
    "square_feet": 2200
  }'
```

5. **Search properties:**
```bash
curl "http://localhost:5000/api/properties?location=Springfield&min_price=400000&bedrooms=4"
```

## Production Considerations

- Change the `SECRET_KEY` to a secure random string
- Use a production database (PostgreSQL, MySQL)
- Enable HTTPS
- Implement rate limiting
- Add logging
- Use environment variables for configuration
- Set up proper error monitoring