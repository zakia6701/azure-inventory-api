import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import get_connection, init_db

app = FastAPI(title="Inventory API")

init_db()


class Product(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int


@app.get("/")
def read_root():
    return {"message": "Inventory API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/products", status_code=201)
def create_product(product: Product):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO products (name, sku, price, quantity) VALUES (?, ?, ?, ?)",
            (product.name, product.sku, product.price, product.quantity),
        )
        conn.commit()
        product_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="SKU already exists")
    finally:
        conn.close()
    return {"id": product_id, **product.model_dump()}


@app.get("/products")
def list_products():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(row)
