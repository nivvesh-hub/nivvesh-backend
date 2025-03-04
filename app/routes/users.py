from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_db
from models.users import User
from models.user_requirements import Requirement
from app.schemas import UserCreate
from app.schemas import Requirement
router = APIRouter(prefix="/users", tags=["Users"])
from passlib.context import CryptContext
from auth import auth

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import random
import requests
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr

# Initialize FastAPI
app = FastAPI()

# Redis for OTP storage (only needed for manual OTP)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# MSG91 Configuration
MSG91_AUTH_KEY = "your-msg91-auth-key"
MSG91_SENDER_ID = "YOUR_SENDER_ID"
MSG91_ROUTE = "4"  # Transactional SMS route
OTP_EXPIRY = 300  # 5 minutes
USE_AUTO_OTP = False  # Change to True if you want MSG91 to generate OTP

# Request Model
class SendOTPRequest(BaseModel):
    phone: constr(regex=r"^\+91[6-9]\d{9}$")  # Valid Indian phone number

# Generate OTP (Only for Manual Mode)
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP via MSG91 (Manual & Auto Mode)
def send_otp_via_msg91(phone: str, otp: str = None):
    url = "https://control.msg91.com/api/v5/otp"
    headers = {
        "authkey": MSG91_AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "mobile": phone,
        "sender": MSG91_SENDER_ID,
        "otp_expiry": OTP_EXPIRY // 60
    }

    # If using manual OTP, include generated OTP in payload
    if not USE_AUTO_OTP and otp:
        payload["otp"] = otp

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# API Endpoint: Send OTP
@app.post("/send-otp")
def send_otp(request: SendOTPRequest):
    otp = None

    # if not USE_AUTO_OTP:
    #     otp = generate_otp()
    #     # redis_client.setex(request.phone, OTP_EXPIRY, otp)  # Store OTP in Redis

    # response = send_otp_via_msg91(request.phone, otp)

    # if response.get("type") != "success":
    #     raise HTTPException(status_code=400, detail="Failed to send OTP")

    return {"message": "OTP sent successfully"}

class VerifyOTPRequest(SendOTPRequest):
    otp: constr(min_length=6, max_length=6)  # OTP must be 6 digits

@app.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    # Use MSG91's OTP Verification API
    # url = f"https://control.msg91.com/api/v5/otp/verify?mobile={request.phone}&otp={request.otp}"
    # headers = {"authkey": MSG91_AUTH_KEY}
    # response = requests.get(url, headers=headers).json()

    # if response.get("type") != "success":
    #     raise HTTPException(status_code=400, detail="Invalid OTP")


        # Check if customer exists in DB
    customer = db.query(User).filter(User.phone == request.phone).first()

    if not customer:
        # Create new customer if not found
        customer_data = User(
            phone=request.phone,
            first_name="Unknown",  # Default values or get from the request if needed
            last_name="Unknown",   # Default values or get from the request if needed
            age=None,              # Default or get from the request
        )
        db.add(customer_data)
        db.commit()
        db.refresh(customer_data)  # Ensure the customer data is refreshed after insert
        customer = customer_data



@router.post("/login")
def login(phone: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth.create_access_token({"sub": str(user.id)}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserCreate)
def get_profile(current_user: User = Depends(auth.get_current_user)):
    return current_user

@router.post("/onboard", response_model=UserCreate)
def onboard_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user

@router.post("/users/requirements/", response_model=Requirement)
def create_requirement_for_user(
    user_id: int, 
    requirement: Requirement, 
    db: Session = Depends(get_db)
):
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the new requirement
    db_requirement = Requirement(
        user_id=user_id,
        description=requirement.description,
        amount=requirement.amount,
        duration=requirement.duration
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    
    return db_requirement
