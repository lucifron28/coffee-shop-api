# ☕ Coffee Shop API

A production-ready FastAPI application for managing a coffee shop: JWT auth, product catalog, orders, and admin endpoints.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-blue.svg)](https://postgresql.org)
[![Heroku](https://img.shields.io/badge/Deploy-Heroku-purple.svg)](https://heroku.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Live docs: https://lucifron-coffee-shop-api-a48f8ef1eb6e.herokuapp.com/docs

## Features

- Authentication & security
	- JWT authentication, role-based access (user/admin)
	- Bcrypt password hashing and validation rules
	- Rate limiting, CORS, and security headers
	- Pydantic validation and consistent error responses
- Products
	- CRUD for coffee products
	- Search by name/description; filter by category, availability, featured
	- Size variants with pricing; pagination (skip/limit)
- Orders
	- Create orders with automatic totals by size and quantity
	- Get user order history and details
	- Admin can update order status (pending → preparing → ready → completed/cancelled)
- Admin
	- Manage users (toggle admin/active)
	- List all orders and basic stats (users, products, orders, pending)
- Monitoring
	- Health checks and DB connectivity; basic metrics endpoint

## Tech stack

- FastAPI (Python 3.11)
- SQLAlchemy ORM (sync)
- Pydantic v2 for schemas
- JWT (python-jose), passlib[bcrypt]
- Rate limiting (slowapi)
- PostgreSQL (production) / SQLite (development)
- Uvicorn/Gunicorn server

## API endpoints

Note: Product, order, and admin routes are prefixed with `/api/v1`. Auth and monitoring are at the root.

### Authentication
- POST `/auth/register` — Register new user
- POST `/auth/token` — Login and get JWT token
- GET `/auth/me` — Current user info

### Products
- GET `/api/v1/products` — List products (filters: skip, limit, category, featured, available)
- GET `/api/v1/products/search` — Search products (?q=term)
- GET `/api/v1/products/categories` — Available categories
- GET `/api/v1/products/{id}` — Product details
- POST `/api/v1/products` — Create product (admin)
- PUT `/api/v1/products/{id}` — Update product (admin)
- DELETE `/api/v1/products/{id}` — Delete product (admin)

### Orders
- POST `/api/v1/orders` — Create order (auth)
- GET `/api/v1/orders` — User's orders (auth)
- GET `/api/v1/orders/{id}` — Order details (auth)
- PATCH `/api/v1/orders/{id}/status` — Update order status (admin)

### Admin
- GET `/api/v1/admin/users` — List all users (admin)
- PATCH `/api/v1/admin/users/{id}/admin` — Toggle admin status (admin)
- PATCH `/api/v1/admin/users/{id}/active` — Toggle user active status (admin)
- GET `/api/v1/admin/orders` — List all orders (admin)
- GET `/api/v1/admin/stats` — System stats (admin)

### Monitoring
- GET `/health` — Health check
- GET `/health/db` — Database health
- GET `/metrics` — Basic metrics

## Project structure

```
coffee-shop-api/
├── app/
│   ├── main.py            # FastAPI app, router registration
│   ├── config.py          # Settings and env parsing
│   ├── database.py        # Engine/session and init_db
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic v2 schemas
│   ├── middleware.py      # CORS, rate limit, security, logging
│   ├── monitoring.py      # /health, /health/db, /metrics
│   ├── auth_router.py     # Auth endpoints
│   ├── product_router.py  # Product endpoints
│   ├── order_router.py    # Order endpoints
│   └── admin_router.py    # Admin endpoints
├── data/
│   └── processed_coffee_products.json
├── requirements.txt
├── Procfile               # Web + release phase
├── runtime.txt            # Python version
├── release.py             # DB init + seed/update
└── load_products.py       # Local data loader
```

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

- FastAPI, SQLAlchemy, and Pydantic communities
- Everyone who loves great coffee ☕