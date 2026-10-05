from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Inventory API")


class Product(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int


products: dict[int, Product] = {}
next_id = 1


@app.get("/")
def read_root():
    return {"message": "Inventory API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/products", status_code=201)
def create_product(product: Product):
    global next_id
    products[next_id] = product
    next_id += 1
    return {"id": next_id - 1, **product.model_dump()}


@app.get("/products")
def list_products():
    return [{"id": pid, **p.model_dump()} for pid, p in products.items()]


@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product_id, **products[product_id].model_dump()}
