#!/usr/bin/env python3
"""
Heroku release script to run database migrations and seed data
"""
import os
import sys
import json
from sqlalchemy.orm import Session

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.models import CoffeeProduct, User
from app.database import SessionLocal, init_db
from app.auth_router import get_password_hash

def run_migrations():
    """Initialize database tables"""
    print("🔄 Initializing database...")
    init_db()
    print("✅ Database initialized")

def seed_products():
    """Load coffee products if they don't exist"""
    db: Session = SessionLocal()
    try:
        existing_count = db.query(CoffeeProduct).count()
        
        products_file = "data/processed_coffee_products.json"
        if not os.path.exists(products_file):
            print("⚠️  No products file found, skipping product seeding")
            return
            
        with open(products_file, 'r') as f:
            products = json.load(f)
        
        if existing_count > 0:
            print(f"📦 Products already exist ({existing_count} products)")
            print("🔄 Updating product categories...")
            
            # Update existing products with new categories
            for prod in products:
                existing_product = db.query(CoffeeProduct).filter(CoffeeProduct.name == prod['name']).first()
                if existing_product:
                    existing_product.category = prod['category']
                    
            db.commit()
            print("✅ Updated product categories")
            return
        
        print("📦 Loading coffee products...")
        
        for prod in products:
            prod_data = prod.copy()
            prod_data.pop('id', None)
            db_product = CoffeeProduct(**prod_data)
            db.add(db_product)
        
        db.commit()
        print(f"✅ Loaded {len(products)} coffee products")
        
    except Exception as e:
        print(f"❌ Error seeding products: {e}")
        db.rollback()
    finally:
        db.close()

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    db: Session = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            print("👤 Admin user already exists")
            return
        
        admin_password = os.getenv("ADMIN_PASSWORD", "CoffeeAdmin123!")
        hashed_password = get_password_hash(admin_password)
        
        admin_user = User(
            username="admin",
            email="admin@coffeeshop.com",
            hashed_password=hashed_password,
            is_active=True,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        print("✅ Created admin user (username: admin)")
        print(f"🔑 Admin password: {admin_password}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Running Heroku release tasks...")
    
    run_migrations()
    seed_products()
    create_admin_user()
    
    print("✅ Release tasks completed!")
