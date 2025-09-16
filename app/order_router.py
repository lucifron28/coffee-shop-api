from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from .auth_router import get_user
from .middleware import limiter
from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from .auth_router import get_user
    from jose import JWTError, jwt
    from .config import settings
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user

def calculate_order_total(items: List[schemas.OrderItem], db: Session):
    total = 0.0
    for item in items:
        product = db.query(models.CoffeeProduct).filter(models.CoffeeProduct.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        # Get price based on size
        size_key = item.size.lower().replace(" ", "_").replace("(", "").replace(")", "")
        if "small" in size_key or "8oz" in size_key:
            price = product.prices.get("small", 0)
        elif "medium" in size_key or "12oz" in size_key:
            price = product.prices.get("medium", 0)
        elif "large" in size_key or "16oz" in size_key:
            price = product.prices.get("large", 0)
        elif "single" in size_key:
            price = product.prices.get("single", 0)
        elif "double" in size_key:
            price = product.prices.get("double", 0)
        else:
            price = product.prices.get("small", 0)  # Default to small
        
        total += price * item.quantity
    
    return total

@router.post("/orders", response_model=schemas.Order)
@limiter.limit("10/minute")
def create_order(request: Request, order: schemas.OrderCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Calculate total price
    total_price = calculate_order_total(order.items, db)
    
    # Create order
    db_order = models.Order(
        user_id=current_user.id,
        items=[item.dict() for item in order.items],
        total_price=total_price,
        status="pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return schemas.Order(
        id=db_order.id,
        user_id=db_order.user_id,
        items=order.items,
        total_price=db_order.total_price,
        status=db_order.status,
        created_at=db_order.created_at.isoformat()
    )

@router.get("/orders", response_model=List[schemas.Order])
def get_user_orders(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.id).all()
    return [
        schemas.Order(
            id=order.id,
            user_id=order.user_id,
            items=[schemas.OrderItem(**item) for item in order.items],
            total_price=order.total_price,
            status=order.status,
            created_at=order.created_at.isoformat()
        ) for order in orders
    ]

@router.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return schemas.Order(
        id=order.id,
        user_id=order.user_id,
        items=[schemas.OrderItem(**item) for item in order.items],
        total_price=order.total_price,
        status=order.status,
        created_at=order.created_at.isoformat()
    )

@router.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    valid_statuses = ["pending", "preparing", "ready", "completed", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    order.status = status
    db.commit()
    
    return {"message": f"Order {order_id} status updated to {status}"}
