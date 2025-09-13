from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
import sys

router = APIRouter()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Coffee Shop API",
        "version": "1.0.0"
    }

@router.get("/health/db")
def db_health_check():
    """Database health check"""
    try:
        from .database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logging.error(f"Database health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database unavailable")

@router.get("/metrics")
def get_metrics():
    """Basic metrics endpoint"""
    # In production, you might use Prometheus metrics here
    return {
        "uptime": "placeholder",
        "requests_total": "placeholder",
        "active_connections": "placeholder"
    }
