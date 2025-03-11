from fastapi import APIRouter
from app.services.tarraki.auth import get_access_token
from app.schemas.tarraki.auth import TokenResponse

router = APIRouter()

@router.get("/token", response_model=TokenResponse)
def fetch_token():
    return get_access_token()
