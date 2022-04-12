from fastapi import FastAPI

from config import BASE_SC_SERVER_URL
from json_client import client
from server import admin, auth
from log import get_default_logger


log = get_default_logger(__name__)

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router)

client.connect(BASE_SC_SERVER_URL)
if client.is_connected():
    log.info("Connection with sc-server established successfully")
else:
    log.warning("Connection with sc-server not established. Run auth-server in DB-only mode")
