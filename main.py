import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Literal
from database import db, create_document, get_documents
from schemas import Merchant, Customer, Driver
from hashlib import sha256

app = FastAPI(title="DropLine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def hash_password(pw: str) -> str:
    return sha256(pw.encode("utf-8")).hexdigest()


class RegisterMerchant(BaseModel):
    shop_name: str
    category: str
    city: str
    address: str
    email: EmailStr
    phone: str
    password: str


class RegisterCustomer(BaseModel):
    full_name: str
    city: str
    address: str
    email: EmailStr
    phone: str
    password: str


class RegisterDriver(BaseModel):
    full_name: str
    city: str
    vehicle_type: str
    vehicle_plate: str | None = None
    email: EmailStr
    phone: str
    national_id: str | None = None
    password: str


class LoginRequest(BaseModel):
    role: Literal["merchant", "customer", "driver"]
    email: EmailStr
    password: str


@app.get("/")
def root():
    return {"name": "DropLine API", "status": "ok"}


@app.post("/auth/register/merchant")
def register_merchant(payload: RegisterMerchant):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")

    existing = db["merchant"].find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    doc = Merchant(
        shop_name=payload.shop_name,
        category=payload.category,
        city=payload.city,
        address=payload.address,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
    )
    inserted_id = create_document("merchant", doc)
    return {"id": inserted_id, "message": "Merchant registered"}


@app.post("/auth/register/customer")
def register_customer(payload: RegisterCustomer):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")

    existing = db["customer"].find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    doc = Customer(
        full_name=payload.full_name,
        city=payload.city,
        address=payload.address,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
    )
    inserted_id = create_document("customer", doc)
    return {"id": inserted_id, "message": "Customer registered"}


@app.post("/auth/register/driver")
def register_driver(payload: RegisterDriver):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")

    existing = db["driver"].find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    doc = Driver(
        full_name=payload.full_name,
        city=payload.city,
        vehicle_type=payload.vehicle_type,
        vehicle_plate=payload.vehicle_plate,
        email=payload.email,
        phone=payload.phone,
        national_id=payload.national_id,
        password_hash=hash_password(payload.password),
    )
    inserted_id = create_document("driver", doc)
    return {"id": inserted_id, "message": "Driver registered"}


@app.post("/auth/login")
def login(payload: LoginRequest):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")

    collection = payload.role
    user = db[collection].find_one({"email": payload.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.get("password_hash") != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Simple session token (demo). In production, use JWT.
    token = sha256(f"{payload.email}:{payload.role}".encode()).hexdigest()
    return {
        "message": "Login successful",
        "token": token,
        "role": payload.role,
        "profile": {
            "id": str(user.get("_id")),
            "email": user.get("email"),
        },
    }


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available" if db is None else "✅ Connected",
    }
    try:
        if db is not None:
            response["collections"] = db.list_collection_names()
    except Exception as e:
        response["database"] = f"⚠️  Error: {str(e)[:60]}"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
