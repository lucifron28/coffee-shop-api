
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from .database import init_db
from .product_router import router as product_router
from .auth_router import router as auth_router
from .order_router import router as order_router
from .monitoring import router as monitoring_router
from .middleware import setup_middleware
from .config import settings
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Coffee Shop API",
    description="A production-ready coffee shop management API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup middleware
app = setup_middleware(app, settings)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.on_event("startup")
def on_startup():
    init_db()
    logging.info("Coffee Shop API started successfully")

@app.on_event("shutdown")
def on_shutdown():
    logging.info("Coffee Shop API shutting down")

# Include routers
app.include_router(monitoring_router, tags=["monitoring"])
app.include_router(auth_router, tags=["authentication"])
app.include_router(product_router, prefix="/api/v1", tags=["products"])
app.include_router(order_router, prefix="/api/v1", tags=["orders"])

# Import and include admin router
from .admin_router import router as admin_router
app.include_router(admin_router, prefix="/api/v1", tags=["admin"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Coffee Shop API!",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
