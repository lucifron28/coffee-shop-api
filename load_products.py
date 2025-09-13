import json
from sqlalchemy.orm import Session
from app.models import CoffeeProduct
from app.database import SessionLocal, init_db

def load_products(json_path):
    with open(json_path, 'r') as f:
        products = json.load(f)
    db: Session = SessionLocal()
    for prod in products:
        # Remove id to let DB autoincrement
        prod_data = prod.copy()
        prod_data.pop('id', None)
        db_product = CoffeeProduct(**prod_data)
        db.add(db_product)
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    load_products("data/processed_coffee_products.json")
    print("Products loaded into database.")
