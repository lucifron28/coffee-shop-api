from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, validator
import re

class PriceModel(BaseModel):
    small: Optional[float] = None
    medium: Optional[float] = None
    large: Optional[float] = None
    single: Optional[float] = None
    double: Optional[float] = None

class CoffeeProductBase(BaseModel):
    name: str
    image: Optional[str] = None
    original_ingredients: Optional[List[str]] = None
    ingredients: List[str]
    category: str
    description: str
    prices: PriceModel
    sizes: List[str]
    caffeine_mg: int
    calories: int
    is_featured: bool = False
    is_available: bool = True
    preparation_time: int
    customizations: List[str]
    rating: float
    review_count: int

    @validator('rating')
    def validate_rating(cls, v):
        if not 0 <= v <= 5:
            raise ValueError('Rating must be between 0 and 5')
        return v

class CoffeeProductCreate(CoffeeProductBase):
    pass

class CoffeeProduct(CoffeeProductBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        return v

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class OrderItem(BaseModel):
    product_id: int
    size: str
    quantity: int = 1
    customizations: Optional[List[str]] = []

    @validator('quantity')
    def validate_quantity(cls, v):
        if v < 1:
            raise ValueError('Quantity must be at least 1')
        return v

class OrderCreate(BaseModel):
    items: List[OrderItem]

class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total_price: float
    status: str = "pending"
    created_at: str

