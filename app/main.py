
from fastapi import FastAPI
from .database import init_db
from .product_router import router as product_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(product_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Coffee Shop API!"}
