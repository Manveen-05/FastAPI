import json
from pathlib import Path
from typing import List , Dict

# Define the absolute path to the products.json data file based on this script's location
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"

def load_products() -> List[Dict]:
    """Helper function to load the product dataset from the JSON file."""
    # Check if the data file exists to prevent a crash when trying to read it
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Products data file not found at: {DATA_FILE}")
    
    # Open the file with UTF-8 encoding and parse the JSON array into a Python list
    with open(DATA_FILE , "r",encoding="utf-8") as f:
        return json.load(f)


def get_all_products() -> List[Dict]:



    """Retrieves all products by loading them from the data source."""
    # Fetch the product list and return it to the caller
    products = load_products()
    return products    

def save_products(products: List[Dict]) -> None:
    with open(DATA_FILE , "w",encoding="utf-8") as f:
        json.dump(products , f , indent=2 , ensure_ascii=False)

def add_product(product: Dict) -> Dict:
    """Appends a new product to the list and saves to the JSON file."""
    products = get_all_products()
    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("Product with same SKU already exists")
    products.append(product)
    save_products(products)
    return product


def update_product(product_id: str , product_data: Dict) -> Dict:
    """Performs a partial deep update on a product, handling nested dictionaries safely."""
    products = get_all_products()
    for prod in products:
        if prod["id"] == str(product_id):
            # Shallow copy to avoid modifying original while iterating
            update_data = dict(product_data)
            if "dimensions_cm" in update_data and update_data["dimensions_cm"]:
                prod.setdefault("dimensions_cm", {}).update(update_data["dimensions_cm"])
                update_data.pop("dimensions_cm")
            
            if "seller" in update_data and update_data["seller"]:
                prod.setdefault("seller", {}).update(update_data["seller"])
                update_data.pop("seller")

            prod.update(update_data)
            save_products(products)
            return prod
    raise ValueError("Product not found")


def delete_product(product_id: str) -> Dict:
    """Removes a product from the dataset by its UUID."""
    products = get_all_products()
    for idx , product in enumerate(products):
        if product["id"] == str(product_id):
            deleted = products.pop(idx)
            save_products(products)
            return {"message" : "Product deleted successfully" , "product" : deleted}
    raise ValueError("Product not found")