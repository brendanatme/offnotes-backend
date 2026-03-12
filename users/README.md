# Users App

The Users app provides API endpoints for managing user accounts in the OffNotes application.

## Features

- **User CRUD Operations**: Create, read, update, and delete user accounts
- **Password Hashing**: Secure password handling with Django's built-in hashing
- **Authentication Required**: All endpoints require valid authentication tokens
- **RESTful API**: Standard REST endpoints for user management

## API Endpoints

### User List & Create
- **GET** `/api/users/` - List all users (paginated)
- **POST** `/api/users/` - Create a new user

### User Detail, Update & Delete
- **GET** `/api/users/{id}/` - Retrieve a specific user
- **PUT** `/api/users/{id}/` - Update a user completely
- **PATCH** `/api/users/{id}/` - Partially update a user
- **DELETE** `/api/users/{id}/` - Delete a user

## User Fields

- `id` (read-only): User ID
- `username`: Unique username (required for creation)
- `email`: User email address
- `first_name`: User's first name
- `last_name`: User's last name
- `password`: User password (write-only, hashed)
- `is_active`: Whether the user account is active
- `date_joined` (read-only): Account creation timestamp

## Example Requests

### Create a User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123"
  }'
```

### List All Users
```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Update a User
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "email": "newemail@example.com",
    "first_name": "Jonathan"
  }'
```

## Authentication

All user endpoints require authentication using Django REST Framework's Token Authentication. Include the token in the Authorization header:

```
Authorization: Token <your_token_here>
```

## Best Practices

1. **Password Security**: 
   - Never expose passwords in responses (write-only field)
   - Always use HTTPS in production
   - Enforce strong password requirements

2. **Permissions**:
   - Currently restricted to authenticated users
   - Consider implementing role-based permissions for production

3. **Data Validation**:
   - Username must be unique
   - Email format is validated
   - Passwords are hashed using Django's default algorithm

## Implementation Details

- **Model**: Uses Django's built-in `User` model
- **Serializer**: `UserSerializer` handles data serialization and password hashing
- **ViewSet**: `UserViewSet` provides full CRUD functionality
- **Router**: Automatic URL routing via DRF's `DefaultRouter`
