from fastapi.openapi.models import EmailStr
from pydantic import BaseModel, Field , AnyUrl , field_validator , model_validator, computed_field
from typing import Annotated, List , Literal , Optional
from uuid import UUID 
from datetime import datetime



class Dimensions(BaseModel):
    length: Annotated[float, Field(description="Length in cm", ge=0)]
    width: Annotated[float, Field(description="Width in cm", ge=0)]
    height: Annotated[float, Field(description="Height in cm", ge=0)]

class Seller(BaseModel):
    seller_id: UUID
    name: Annotated[str, Field(description="Seller name", min_length=1, max_length=100)]
    email: EmailStr
    website: AnyUrl

    @field_validator("email" , mode="after")
    @classmethod
    def validate_email(cls, value: str):
        if "@" not in value:
            raise ValueError("Email must contain @")
        return value
    
    @field_validator("website" , mode="after")
    @classmethod
    def validate_website(cls, value: AnyUrl):
        if str(value).startswith("http://") or str(value).startswith("https://"):
            return value
        raise ValueError("Website must contain http or https")

class Product(BaseModel):
    id: UUID
    sku: Annotated[str, Field(min_length=3, max_length=50, description="Stock Keeping Unit", examples=["XIAO-359GB-001"])]
    name: Annotated[str, Field(description="Product name", min_length=1, max_length=100)]
    description: Annotated[str, Field(description="Product description", min_length=1, max_length=1000)]
    category: Annotated[str, Field(description="Product category", min_length=1, max_length=50)]
    brand: Annotated[str, Field(description="Product brand", min_length=1, max_length=50)]
    price: Annotated[float, Field(description="Product price", ge=0)]
    currency: Annotated[str, Field(description="Currency code", min_length=3, max_length=3, examples=["INR"])]
    discount_percent: Annotated[float, Field(description="Discount percentage", ge=0, le=100)]
    stock: Annotated[int, Field(description="Product stock", ge=0, examples=[10])]
    is_active: Annotated[bool, Field(description="Is the product active", default=True)]
    rating: Annotated[float, Field(description="Product rating", ge=0, le=5)]
    tags: Annotated[List[str], Field(description="List of product tags", default_factory=list)]
    image_urls: Annotated[List[str], Field(description="List of product image URLs", default_factory=list)]
    dimensions_cm: Dimensions
    seller: Seller
    created_at: datetime

    @field_validator("sku" , mode="after")
    @classmethod
    def validate_sku(cls, value: str):
        if "-" not in value:
            raise ValueError("SKU must have '- '")
        last = value.split("-")[-1]
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with a 3-digit number (example: SKU-XXX)")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_buisness_rules(cls , model : "Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("Product with 0 stock cannot be active")
        if model.discount_percent > 0 and model.rating < 3:
            raise ValueError("Product with discount must have a rating greater than 0")
        return model
    

    @computed_field
    @property
    def final_price(self) -> float:
        """Calculates the final price after discount."""
        return self.price * (1 - self.discount_percent / 100)

    @computed_field
    @property
    def volume_cubic_meters(self) -> float:
        """Calculates the volume of the product in cubic meters."""
        return round((self.dimensions_cm.length * self.dimensions_cm.width * self.dimensions_cm.height) / 1000000, 6)

class DimensionsUpdate(BaseModel):
    """Schema for partially updating product dimensions. All fields are optional."""
    length: Optional[float] = Field(default=None, description="Length in cm", ge=0)
    width: Optional[float] = Field(default=None, description="Width in cm", ge=0)
    height: Optional[float] = Field(default=None, description="Height in cm", ge=0)

class SellerUpdate(BaseModel):
    """Schema for partially updating seller details. All fields are optional."""
    seller_id: Optional[UUID] = None
    name: Optional[str] = Field(default=None, description="Seller name", min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    website: Optional[AnyUrl] = None

    @field_validator("email", mode="after")
    @classmethod
    def validate_email(cls, value: Optional[str]):
        if value is not None and "@" not in value:
            raise ValueError("Email must contain @")
        return value
    
    @field_validator("website", mode="after")
    @classmethod
    def validate_website(cls, value: Optional[AnyUrl]):
        if value is not None and not (str(value).startswith("http://") or str(value).startswith("https://")):
            raise ValueError("Website must contain http or https")
        return value

class ProductUpdate(BaseModel):
    """Schema for partially updating a product. Includes nested optional updates and excludes stock."""
    sku: Optional[str] = Field(default=None, min_length=3, max_length=50, description="Stock Keeping Unit")
    name: Optional[str] = Field(default=None, description="Product name", min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, description="Product description", min_length=1, max_length=1000)
    category: Optional[str] = Field(default=None, description="Product category", min_length=1, max_length=50)
    brand: Optional[str] = Field(default=None, description="Product brand", min_length=1, max_length=50)
    price: Optional[float] = Field(default=None, description="Product price", ge=0)
    currency: Optional[str] = Field(default=None, description="Currency code", min_length=3, max_length=3)
    discount_percent: Optional[float] = Field(default=None, description="Discount percentage", ge=0, le=100)
    is_active: Optional[bool] = Field(default=None, description="Is the product active")
    rating: Optional[float] = Field(default=None, description="Product rating", ge=0, le=5)
    tags: Optional[List[str]] = Field(default=None, description="List of product tags")
    image_urls: Optional[List[str]] = Field(default=None, description="List of product image URLs")
    dimensions_cm: Optional[DimensionsUpdate] = None
    seller: Optional[SellerUpdate] = None

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku(cls, value: Optional[str]):
        if value is not None:
            if "-" not in value:
                raise ValueError("SKU must have '-'")
            last = value.split("-")[-1]
            if not (len(last) == 3 and last.isdigit()):
                raise ValueError("SKU must end with a 3-digit number (example: SKU-XXX)")
        return value