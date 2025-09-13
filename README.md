# Coffee Shop API

# ☕ Coffee Shop API

A FastAPI application for managing a coffee shop's operations, featuring JWT authentication, order management, product catalog, and comprehensive admin functionality.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-blue.svg)](https://postgresql.org)
[![Heroku](https://img.shields.io/badge/Deploy-Heroku-purple.svg)](https://heroku.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

### 🔐 Authentication & Security
- **JWT Authentication** with secure token-based auth
- **Role-based Access Control** (User/Admin permissions)
- **Password Security** with bcrypt hashing and validation rules
- **Rate Limiting** to prevent API abuse
- **CORS Protection** with configurable origins
- **Input Validation** with Pydantic models

### 📦 Product Management
- **Full CRUD Operations** for coffee products
- **Advanced Search & Filtering** by category, price, availability
- **Product Categories** (espresso, latte, cappuccino, etc.)
- **Size Variants** with different pricing
- **Stock Management** with availability tracking

### 🛒 Order System
- **Order Placement** with automatic total calculation
- **Order History** for customers
- **Order Status Tracking** (pending, confirmed, completed, cancelled)
- **Admin Order Management** with status updates
- **Detailed Order Items** with size and quantity

### 👨‍💼 Admin Dashboard
- **User Management** (view, activate/deactivate, promote to admin)
- **Order Overview** with filtering and status management
- **System Statistics** (user count, order metrics, revenue)
- **Product Administration** (create, update, delete products)

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: JWT with python-jose
- **ORM**: SQLAlchemy with async support
- **Validation**: Pydantic v2
- **Deployment**: Heroku with Gunicorn + Uvicorn
- **Security**: Passlib, bcrypt, rate limiting


## 📊 API Endpoints

### 🔐 Authentication
```
POST   /auth/register          Register new user
POST   /auth/login             Login and get JWT token  
GET    /auth/me                Get current user profile
PUT    /auth/me                Update user profile
```

### ☕ Products
```
GET    /products/              List products (with pagination & filters)
GET    /products/search        Search products by name/description
GET    /products/categories    Get available categories
GET    /products/{id}          Get product details
POST   /products/              Create product (admin only)
PUT    /products/{id}          Update product (admin only)
DELETE /products/{id}          Delete product (admin only)
```

### 🛒 Orders
```
POST   /orders/                Create new order
GET    /orders/                Get user's order history
GET    /orders/{id}            Get order details
PATCH  /orders/{id}/status     Update order status (admin only)
```

### 👨‍💼 Admin
```
GET    /admin/users            List all users
PATCH  /admin/users/{id}/admin Toggle admin status
PATCH  /admin/users/{id}/active Toggle user status
GET    /admin/orders           List all orders
GET    /admin/stats            Get system statistics
```

### 🔍 Monitoring
```
GET    /health                 API health check
GET    /health/db              Database connectivity check
```

## 📁 Project Structure

```
coffee-shop-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and middleware
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection and setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── middleware.py        # Custom middleware
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── products.py      # Product management
│       ├── orders.py        # Order management
│       └── admin.py         # Admin functionality
├── data/
│   └── processed_coffee_products.json
├── requirements.txt
├── Procfile                 # Heroku configuration
├── runtime.txt             # Python version
├── release.py              # Database seeding script
└── load_products.py        # Initial data loader
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing framework
- [SQLAlchemy](https://sqlalchemy.org/) for the ORM
- [Pydantic](https://pydantic.dev/) for data validation
- Coffee enthusiasts everywhere ☕

---

**🔗 Live Demo**: [https://lucifron-coffee-shop-api-a48f8ef1eb6e.herokuapp.com/docs](https://lucifron-coffee-shop-api-a48f8ef1eb6e.herokuapp.com/docs)


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