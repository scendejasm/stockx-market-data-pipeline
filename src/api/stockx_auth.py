# src/api/stockx_auth.py
import os
import requests
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv

# from src.config import EBAY_APP_ID

load_dotenv()
router = APIRouter()


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL")

scope = 'offline_access openid'
state = 'secureRandomeState123'

@router.get("/login")
async def login():
    auth_url = generate_auth0_login_url()

    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def callback(request:Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=404, details="Missing authorization code")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': CALLBACK_URL
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        tokens = response.json()
        request.session["ACCESS_TOKEN"] = tokens.get("access_token")
        request.session["REFRESH_TOKEN"] = tokens.get("refresh_token")
        return JSONResponse(content={
                "access_token": tokens.get("access_token"),
                "refresh_token": tokens.get("refresh_token"),
                "id_token": tokens.get("id_token"),
                "expires_in": tokens.get("expires_in")
            })

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


def generate_auth0_login_url():

    login_url = (
        f"https://{AUTH0_DOMAIN}/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={CALLBACK_URL}"
        f"&scope={scope}"
        f"&state={state}"
    )
    print(f"Using login url of: {login_url}")
    return login_url


@router.get("/use-token")
async def use_token(request: Request):
    token = request.session.get("REFRESH_TOKEN")
    if not token:
        return {"error": "Badges, we don't need no stinking Badges"}
    return {"token": token}
