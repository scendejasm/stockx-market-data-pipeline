from fastapi import Fastapi
from starlette.middleware.sessions import SessionMiddleware
from src.apy.stockx_auth import router as auth_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-sesssion-key")
app.include_router(auth_router)
