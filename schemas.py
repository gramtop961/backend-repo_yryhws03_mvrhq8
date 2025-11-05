"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- Candidate -> "candidate" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime

# Example schemas remain available for reference
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# HR Onboarding Portal Schemas
StatusType = Literal[
    "Offer Sent",
    "Accepted",
    "Documents Received",
    "Policy Sent",
    "Welcome Sent",
]

class Candidate(BaseModel):
    """
    Candidates collection schema
    Collection name: "candidate"
    """
    name: str = Field(..., min_length=2, description="Candidate full name")
    email: EmailStr = Field(..., description="Candidate email address")
    role: str = Field(..., description="Role being hired for")
    joining_date: datetime = Field(..., description="Joining date")
    status: StatusType = Field("Offer Sent", description="Current onboarding status")

class CandidateUpdate(BaseModel):
    status: StatusType
