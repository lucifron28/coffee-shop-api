# Heroku Deployment Guide - Coffee Shop API

## Prerequisites
- Heroku CLI installed
- Git repository initialized
- Python 3.11+ locally

## Step 1: Create Heroku App
```bash
# Login to Heroku
heroku login

# Create a new Heroku app (replace 'your-app-name' with your desired name)
heroku create your-coffee-shop-api

# Add PostgreSQL database
heroku addons:create heroku-postgresql:essential-0
```

## Step 2: Set Environment Variables
```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key"
heroku config:set ENVIRONMENT="production"
heroku config:set ALLOWED_ORIGINS="https://your-frontend-domain.com"
heroku config:set ADMIN_PASSWORD="YourSecureAdminPassword123!"
heroku config:set LOG_LEVEL="INFO"

# Optional: Set rate limiting
heroku config:set RATE_LIMIT_REQUESTS="200"
```

## Step 3: Deploy
```bash
# Add files to git
git add .
git commit -m "Prepare for Heroku deployment"

# Deploy to Heroku
git push heroku main

# Check deployment logs
heroku logs --tail
```

## Step 4: Verify Deployment
```bash
# Open your app in browser
heroku open

# Check API health
curl https://your-app-name.herokuapp.com/health

# View database info
heroku pg:info

# Check running processes
heroku ps
```

## Step 5: Test Your API
Your API will be available at: `https://your-app-name.herokuapp.com`

- API Documentation: `https://your-app-name.herokuapp.com/docs` (disabled in production)
- Health Check: `https://your-app-name.herokuapp.com/health`
- Products: `https://your-app-name.herokuapp.com/api/v1/products`

## Admin Access
The deployment automatically creates an admin user:
- Username: `admin`
- Password: Set via `ADMIN_PASSWORD` environment variable

## Useful Heroku Commands
```bash
# View logs
heroku logs --tail

# Run database migrations manually
heroku run python release.py

# Access PostgreSQL console
heroku pg:psql

# Scale dynos
heroku ps:scale web=1

# Restart app
heroku restart

# Set up custom domain
heroku domains:add your-domain.com
```

## Environment Variables Reference
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL URL | Auto-set by Heroku |
| `SECRET_KEY` | JWT secret key | **Required** |
| `ENVIRONMENT` | Environment mode | `production` |
| `ALLOWED_ORIGINS` | CORS origins | **Required** |
| `ADMIN_PASSWORD` | Admin user password | **Required** |
| `LOG_LEVEL` | Logging level | `INFO` |
| `RATE_LIMIT_REQUESTS` | Rate limit per minute | `100` |

## Troubleshooting
- **Build fails**: Check `requirements.txt` and Python version in `runtime.txt`
- **Database errors**: Ensure PostgreSQL addon is attached
- **CORS issues**: Set correct `ALLOWED_ORIGINS`
- **Import errors**: Check `release.py` can import app modules

## Security Notes
- Never commit `.env` files with secrets
- Use strong passwords for admin users
- Set appropriate CORS origins for production
- Monitor logs for security issues

Your Coffee Shop API is now production-ready on Heroku! 🚀☕
