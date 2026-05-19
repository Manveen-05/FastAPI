from fastapi import FastAPI, HTTPException, Query, Path , Depends , Request
from fastapi.responses import JSONResponse
from services.products import get_all_products, add_product, save_products, delete_product, update_product
from schema.product import Product, ProductUpdate
from uuid import uuid4, UUID
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the FastAPI application instance
app = FastAPI()

# Define the root endpoint
@app.get("/")
def read_root():
    """Root endpoint returning a greeting and the database path from the environment."""
    # Retrieve the database path configured in the .env file under BASE_URL
    DB_PATH = os.getenv("BASE_URL")
    # Return a structured JSON response with status code 200 OK
    return JSONResponse(
        status_code=200,
        content={"message": "Welcome To FASTAPI-ECOMMERCE API","DB_PATH":DB_PATH}
    )

# @app.get("/products/{product_id}")
# def read_product(product_id: int, q: str | None = None):
#     products = {
#         1: "Laptop",
#         2: "Mouse",
#         3: "Keyboard",
#     }
#     product = products.get(product_id)
#     # raise HTTPException(status_code=404, detail="Product not found")
#     return {"product_id": product_id, "product_name": product}

#@app.get("/products")
#def get_products():
#    products = get_all_products()
#    return products

# Endpoint to list, filter, and sort products
@app.get("/products")
def list_products(
    name: str = Query(default=None, min_length=1, max_length=50, description="search product by name(case insensitive , example = laptop)"),
    sort_by_price: bool = Query(default=False, description="sort products by price"),
    sort_by_rating: bool = Query(default=False, description="sort products by rating"),
    sort_by_stock: bool = Query(default=False, description="sort products by stock"),
    sort_order: str = Query(default="asc", description="sort order (asc or desc)"),
    category: str = Query(default=None, description="filter products by category"),
    min_price: float = Query(default=None, description="filter products by minimum price"),
    max_price: float = Query(default=None, description="filter products by maximum price"),
    rating: float = Query(default=None, description="filter products by minimum rating"),
    limit: int = Query(default=None, ge=1, description="limit the number of results returned"),
    offset: int = Query(default=0, ge=0, description="number of results to skip")
):
    # Retrieve the full list of products
    products = get_all_products()
    
    # --- FILTERS ---
    if name:
        needle = name.strip().lower()
        products = [
            p for p in products 
            if needle in p.get("name", "").lower() 
            or needle in p.get("category", "").lower()
            or needle in p.get("description", "").lower()
            or any(needle in tag.lower() for tag in p.get("tags", []))
        ]

    if category:
        products = [p for p in products if p.get("category", "").lower() == category.lower()]
        
    if min_price is not None:
        products = [p for p in products if p.get("price", 0) >= min_price]
        
    if max_price is not None:
        products = [p for p in products if p.get("price", 0) <= max_price]
        
    if rating is not None:
        products = [p for p in products if p.get("rating", 0) >= rating]

    # If the filtered list is empty, return early
    if not products:
        return {"message": "No products found matching your criteria"}

    # --- SORTING ---
    reverse_sort = (sort_order.lower() == "desc")
    
    # Sort based on the provided flags. Only one will take precedence.
    if sort_by_price:
        products = sorted(products, key=lambda x: x.get("price", 0), reverse=reverse_sort)
    elif sort_by_rating:
        products = sorted(products, key=lambda x: x.get("rating", 0), reverse=reverse_sort)
    elif sort_by_stock:
        products = sorted(products, key=lambda x: x.get("stock", 0), reverse=reverse_sort)

    # Calculate total matching items
    total = len(products)
    # Apply offset and limit for pagination
    start = offset
    end = offset + limit if limit is not None else None
    products = products[start:end]

    return {
        "query": name,
        "total_results": total,
        "returned_results": len(products),
        "items": [Product(**p) for p in products]
    }

@app.get("/products/{product_id}")
def get_product_by_id(product_id: str = Path(..., min_length=36, max_length=36, description="UUID of the product, example: 'a16d0e4b-c73a-4f23-b512-503f89124109'")):
    """Retrieve a single product by its UUID."""
    products = get_all_products()

    for product in products:
        if product["id"] == product_id:
            return Product(**product)

    raise HTTPException(status_code=404, detail="Product not found")



@app.post("/products", status_code=201)
def create_product(product: Product) -> Product:
    """Create a new product, generating a UUID and timestamp automatically."""
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat() + "Z"
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product


@app.delete("/products/{product_id}")
def remove_product(product_id: str = Path(..., min_length=36, max_length=36, description="UUID of the product, example: 'a16d0e4b-c73a-4f23-b512-503f89124109'")):
    """Delete a product by its UUID."""
    try:
        delete_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Product deleted successfully"}

@app.put("/products/{product_id}/stock")
def update_stock(
    product_id: str = Path(..., min_length=36, max_length=36, description="UUID of the product, example: 'a16d0e4b-c73a-4f23-b512-503f89124109'"), 
    quantity: int = Query(..., description="Quantity of stock to add/remove (use negative for removal)")
):
    """Increment or decrement product stock by a specific quantity."""
    products = get_all_products()
    product_found = None
    for p in products:
        if p["id"] == product_id:
            product_found = p
            break
            
    if not product_found:
        raise HTTPException(status_code=404, detail="Product not found")
        
    current_stock = product_found.get("stock", 0)
    new_stock = current_stock + quantity
    if new_stock < 0:
        raise HTTPException(status_code=400, detail=f"Stock cannot be negative. Current stock: {current_stock}, attempted change: {quantity}")
        
    try:
        updated_product = update_product(product_id, {"stock": new_stock})
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Product(**updated_product)



