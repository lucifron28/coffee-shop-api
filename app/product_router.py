from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products", response_model=list[schemas.CoffeeProduct])
def list_products(db: Session = Depends(get_db)):
    products = db.query(models.CoffeeProduct).all()
    return products

@router.get("/products/{product_id}", response_model=schemas.CoffeeProduct)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.CoffeeProduct).filter(models.CoffeeProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=schemas.CoffeeProduct)
def create_product(product: schemas.CoffeeProductCreate, db: Session = Depends(get_db)):
    db_product = models.CoffeeProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/products/{product_id}", response_model=schemas.CoffeeProduct)
def update_product(product_id: int, product: schemas.CoffeeProductCreate, db: Session = Depends(get_db)):
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
    db_product = db.query(models.CoffeeProduct).filter(models.CoffeeProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}
