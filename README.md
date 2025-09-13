# Coffee Shop API - Production Ready

## Installation & Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Environment Configuration:**
Copy `.env` file and update values for production:
```bash
cp .env .env.production
```

Key settings to change in production:
- `SECRET_KEY`: Generate a secure random key
- `DATABASE_URL`: Use PostgreSQL for production
- `ENVIRONMENT`: Set to "production"
- `ALLOWED_ORIGINS`: Set to your frontend domains

3. **Database Setup:**
```bash
# Load initial coffee products
python load_products.py
```

4. **Create Admin User:**
```bash
# Register first user via API, then manually set is_admin=True in database
# Or create via SQL: UPDATE users SET is_admin=TRUE WHERE username='admin';
```

## Running the Application

### Development:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Gunicorn (Recommended for production):
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login (get JWT token)
- `GET /auth/me` - Get current user info

### Products
- `GET /api/v1/products` - List products (with filters)
- `GET /api/v1/products/search?q=term` - Search products
- `GET /api/v1/products/categories` - Get product categories
- `GET /api/v1/products/{id}` - Get specific product
- `POST /api/v1/products` - Create product (admin)
- `PUT /api/v1/products/{id}` - Update product (admin)
- `DELETE /api/v1/products/{id}` - Delete product (admin)

### Orders
- `POST /api/v1/orders` - Create new order
- `GET /api/v1/orders` - Get user's orders
- `GET /api/v1/orders/{id}` - Get specific order
- `PATCH /api/v1/orders/{id}/status` - Update order status (admin)

### Admin
- `GET /api/v1/admin/users` - List all users
- `PATCH /api/v1/admin/users/{id}/admin` - Toggle admin status
- `PATCH /api/v1/admin/users/{id}/active` - Toggle user active status
- `GET /api/v1/admin/orders` - List all orders
- `GET /api/v1/admin/stats` - Get system statistics

### Monitoring
- `GET /health` - Health check
- `GET /health/db` - Database health check
- `GET /metrics` - Basic metrics

## Features

### Security
- JWT authentication with secure tokens
- Password validation (minimum 8 chars, mixed case, numbers)
- Rate limiting (configurable per endpoint)
- CORS protection
- Security headers (XSS, CSRF protection)
- Input validation and sanitization

### Production Features
- Environment-based configuration
- Structured logging
- Error handling and validation
- Database connection pooling
- Health checks
- Metrics endpoint
- Admin functionality

### API Features
- Pagination and filtering
- Product search
- Order management with automatic price calculation
- User role management
- Comprehensive error responses

## Testing

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

Example API usage:

1. **Register a user:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "SecurePass123"}'
```

2. **Login:**
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=SecurePass123"
```

3. **Get products:**
```bash
curl "http://localhost:8000/api/v1/products"
```

4. **Create an order (requires auth token):**
```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product_id": 1, "size": "medium", "quantity": 2}]}'
```

## Deployment

For production deployment:

1. Use a production WSGI server (Gunicorn + Uvicorn)
2. Set up a reverse proxy (Nginx)
3. Use a production database (PostgreSQL)
4. Configure environment variables
5. Set up SSL/TLS certificates
6. Monitor with health checks
7. Set up logging aggregation

Your FastAPI Coffee Shop API is now production-ready! 🚀☕
