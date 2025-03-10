from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.models.users import User
from app.models.user_requirements import Requirement
from app.schemas.users import UserCreate
from passlib.context import CryptContext
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from app.utilities.auth import create_access_token, decode_access_token
import secrets

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/verify-otp")

# from app.auth import auth
class SendOTPRequest(BaseModel):
    phone: str  # Ensure the field names match your request payload


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Initialize FastAPI
app = FastAPI()

# class SendOTPRequest(BaseModel):
#     phone: constr(regex=r"^\+91[6-9]\d{9}$")  # Valid Indian phone number

# Generate OTP (Only for Manual Mode)
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP via MSG91 (Manual & Auto Mode)

# def send_otp_via_msg91(phone: str, otp: str = None):
    # url = "https://control.msg91.com/api/v5/otp"
    # headers = {
    #     "authkey": MSG91_AUTH_KEY,
    #     "Content-Type": "application/json"
    # }
    
    # payload = {
    #     "mobile": phone,
    #     "sender": MSG91_SENDER_ID,
    #     "otp_expiry": OTP_EXPIRY // 60
    # }

    # # If using manual OTP, include generated OTP in payload
    # if not USE_AUTO_OTP and otp:
    #     payload["otp"] = otp

    # response = {}
    # return response.json()

@router.post("/send-otp")
def send_otp(request: SendOTPRequest):
    # otp = None

    # if not USE_AUTO_OTP:
    #     otp = generate_otp()

    # response = send_otp_via_msg91(request.phone, otp)

    # if response.get("type") != "success":
    #     raise HTTPException(status_code=400, detail="Failed to send OTP")

    return {"message": "OTP sent successfully"}

class VerifyOTPRequest(SendOTPRequest):
    otp: constr(min_length=6, max_length=6)  # OTP must be 6 digits
    phone: str

@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    # Check if customer exists in DB

# Generate a 32-byte URL-safe token
    secret_key = secrets.token_urlsafe(32)
    print(secret_key)
    customer = db.query(User).filter(User.phone == request.phone).first()

    if not customer:
        # Create new customer if not found
        customer_data = User(
            phone=request.phone,
        )
        db.add(customer_data)
        db.commit()
        db.refresh(customer_data)  # Ensure the customer data is refreshed after insert
        customer = customer_data
    
    access_token = create_access_token(data={"sub": str(customer.id)})
    return {
        "customer": customer,         # If you want to return customer details
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/onboard", response_model=UserCreate)
def onboard_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_uuid = payload.get("sub")
    # Query the user by UUID. Adjust the filter based on how you store the UUID.
    user = db.query(User).filter(User.uuid == user_uuid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# @router.post("/requirements", response_model=Requirement)
# def create_requirement_for_user(
#     requirement: Requirement,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     # Create a new requirement record linked to the current user
#     new_requirement = Requirement(
#         user_id=current_user.id,
#         description=requirement.description,
#         amount=requirement.amount,
#         duration=requirement.duration
#     )
#     db.add(new_requirement)
#     db.commit()
#     db.refresh(new_requirement)
#     return new_requirement


