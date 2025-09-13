from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from .order_router import get_current_user

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_admin(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

@router.get("/admin/users", response_model=List[schemas.User])
def list_all_users(admin_user: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.patch("/admin/users/{user_id}/admin")
def toggle_admin_status(user_id: int, admin_user: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_admin = not user.is_admin
    db.commit()
    
    return {"message": f"User {user.username} admin status: {user.is_admin}"}

@router.patch("/admin/users/{user_id}/active")
def toggle_user_status(user_id: int, admin_user: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = not user.is_active
    db.commit()
    
    return {"message": f"User {user.username} active status: {user.is_active}"}

@router.get("/admin/orders", response_model=List[schemas.Order])
def list_all_orders(admin_user: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
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

@router.get("/admin/stats")
def get_admin_stats(admin_user: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    total_users = db.query(models.User).count()
    total_products = db.query(models.CoffeeProduct).count()
    total_orders = db.query(models.Order).count()
    pending_orders = db.query(models.Order).filter(models.Order.status == "pending").count()
    
    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders
    }
