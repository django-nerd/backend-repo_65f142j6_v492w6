"""
Database Schemas for DropLine

Each Pydantic model represents a MongoDB collection. Collection name is the
lowercase of the class name (e.g., Merchant -> "merchant").
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal


class BaseUser(BaseModel):
    role: Literal["merchant", "customer", "driver"] = Field(..., description="User role")
    full_name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address (unique per role)")
    phone: str = Field(..., description="Phone number")
    city: str = Field(..., description="City")
    password_hash: str = Field(..., description="Hashed password")


class Merchant(BaseModel):
    role: Literal["merchant"] = Field("merchant", description="Fixed role type")
    shop_name: str = Field(..., description="Store name")
    category: str = Field(..., description="Store category (handmade, crochet, clothing, cosmetics, crafts, etc.)")
    city: str = Field(..., description="City")
    address: str = Field(..., description="Pickup address")
    email: EmailStr = Field(..., description="Email")
    phone: str = Field(..., description="Phone number")
    password_hash: str = Field(..., description="Hashed password")
    delivery_notes: Optional[str] = Field(None, description="Optional delivery notes or instructions")
    working_hours: Optional[str] = Field(None, description="Working hours")


class Customer(BaseModel):
    role: Literal["customer"] = Field("customer", description="Fixed role type")
    full_name: str = Field(..., description="Full name")
    city: str = Field(..., description="City")
    address: str = Field(..., description="Address for delivery")
    email: EmailStr = Field(..., description="Email")
    phone: str = Field(..., description="Phone number")
    password_hash: str = Field(..., description="Hashed password")


class Driver(BaseModel):
    role: Literal["driver"] = Field("driver", description="Fixed role type")
    full_name: str = Field(..., description="Full name")
    city: str = Field(..., description="City of operation")
    vehicle_type: str = Field(..., description="Vehicle type (bike, car, etc.)")
    vehicle_plate: Optional[str] = Field(None, description="Vehicle plate number (if applicable)")
    email: EmailStr = Field(..., description="Email")
    phone: str = Field(..., description="Phone number")
    national_id: Optional[str] = Field(None, description="National ID / License number")
    password_hash: str = Field(..., description="Hashed password")


# Notes:
# - The application will use these schemas for validation and the collections will be named
#   merchant, customer, and driver respectively.
