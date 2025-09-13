from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class PriceModel(BaseModel):
    small: Optional[float]
    medium: Optional[float]
    large: Optional[float]
    single: Optional[float]
    double: Optional[float]

class CoffeeProductBase(BaseModel):
    name: str
    image: Optional[str]
    original_ingredients: Optional[List[str]]
    ingredients: List[str]
    category: str
    description: str
    prices: PriceModel
    sizes: List[str]
    caffeine_mg: int
    calories: int
    is_featured: bool
    is_available: bool
    preparation_time: int
    customizations: List[str]
    rating: float
    review_count: int

class CoffeeProductCreate(CoffeeProductBase):
    pass

class CoffeeProduct(CoffeeProductBase):
    id: int

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

class OrderItem(BaseModel):
    product_id: int
    size: str
    quantity: int
    customizations: Optional[List[str]]

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]
    total_price: float

class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total_price: float
    status: str

