import requests
from app.config import CLIENT_ID, CLIENT_SECRET, TARRAKI_BASEURL
from app.schemas.tarraki.auth import TokenResponse
from fastapi import HTTPException

def get_access_token() -> TokenResponse:
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(TARRAKI_BASEURL/access_token, data=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to get access token")

    return TokenResponse(**response.json())
