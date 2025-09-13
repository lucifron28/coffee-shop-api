from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.types import JSON

Base = declarative_base()

class CoffeeProduct(Base):
    __tablename__ = "coffee_products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image = Column(String)
    original_ingredients = Column(JSON)
    ingredients = Column(JSON)
    category = Column(String)
    description = Column(String)
    prices = Column(JSON)
    sizes = Column(JSON)
    caffeine_mg = Column(Integer)
    calories = Column(Integer)
    is_featured = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    preparation_time = Column(Integer)
    customizations = Column(JSON)
    rating = Column(Float)
    review_count = Column(Integer)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    items = Column(JSON)
    total_price = Column(Float)
    status = Column(String, default="pending")
    user = relationship("User")
