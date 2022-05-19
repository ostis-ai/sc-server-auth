from fastapi import FastAPI
from config import BASE_SC_SERVER_URL
from server import admin, auth
from log import get_default_logger


log = get_default_logger(__name__)

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router)
