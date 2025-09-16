from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from . import schemas, models, database
from .middleware import limiter

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products", response_model=List[schemas.CoffeeProduct])
@limiter.limit("100/minute")
def list_products(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    available: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    query = db.query(models.CoffeeProduct)
    
    if category:
        query = query.filter(models.CoffeeProduct.category == category)
    if featured is not None:
        query = query.filter(models.CoffeeProduct.is_featured == featured)
    if available is not None:
        query = query.filter(models.CoffeeProduct.is_available == available)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/products/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.CoffeeProduct.category).distinct().all()
    return {"categories": [cat[0] for cat in categories]}

@router.get("/products/search")
@limiter.limit("50/minute")
def search_products(
    request: Request,
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    products = db.query(models.CoffeeProduct).filter(
        models.CoffeeProduct.name.contains(q) |
        models.CoffeeProduct.description.contains(q)
    ).all()
    return products

@router.get("/products/{product_id}", response_model=schemas.CoffeeProduct)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.CoffeeProduct).filter(models.CoffeeProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=schemas.CoffeeProduct)
def create_product(product: schemas.CoffeeProductCreate, db: Session = Depends(get_db)):
    # In production, this should require admin authentication
    db_product = models.CoffeeProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/products/{product_id}", response_model=schemas.CoffeeProduct)
def update_product(product_id: int, product: schemas.CoffeeProductCreate, db: Session = Depends(get_db)):
    # In production, this should require admin authentication
    db_product = db.query(models.CoffeeProduct).filter(models.CoffeeProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # In production, this should require admin authentication
    db_product = db.query(models.CoffeeProduct).filter(models.CoffeeProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}
