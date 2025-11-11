"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Company profile schemas for MILDSHIFT PRoject

class Company(BaseModel):
    name: str = Field(..., description="Company name")
    tagline: Optional[str] = Field(None, description="Short company tagline")
    description: Optional[str] = Field(None, description="About the company")
    address: Optional[str] = Field(None, description="Office address")
    phone: Optional[str] = Field(None, description="Contact phone")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    website: Optional[str] = Field(None, description="Website URL")
    hero_image: Optional[str] = Field(None, description="Hero image URL")

class Service(BaseModel):
    title: str = Field(..., description="Service title")
    summary: Optional[str] = Field(None, description="Short summary")
    icon: Optional[str] = Field(None, description="Icon name or URL")
    features: Optional[List[str]] = Field(default_factory=list, description="Key features")

class ProcessStep(BaseModel):
    order: int = Field(..., ge=1, description="Step order (1..n)")
    title: str = Field(..., description="Step title")
    description: Optional[str] = Field(None, description="Step details")
    icon: Optional[str] = Field(None, description="Icon name or URL")

class ContactMessage(BaseModel):
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    subject: str = Field(..., description="Message subject")
    message: str = Field(..., min_length=5, description="Message body")

# Example schemas (kept for reference and potential admin tooling)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
