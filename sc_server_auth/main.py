from fastapi import FastAPI

from sc_server_auth.configs.log import get_default_logger
from sc_server_auth.server import admin, auth

log = get_default_logger(__name__)

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router)
