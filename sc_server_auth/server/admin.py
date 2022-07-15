from dataclasses import asdict

from fastapi.routing import APIRouter

import sc_server_auth.configs.constants as cnt
from sc_server_auth.configs.log import get_file_only_logger
from sc_server_auth.configs.models import Message, Messages
from sc_server_auth.server import models
from sc_server_auth.server.database import DataBase
from sc_server_auth.server.verifiers import password_verifier, username_verifier

log = get_file_only_logger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


def _verify_user_info_in_database(database: DataBase, name: str, password: str) -> Message:
    if not username_verifier(name):
        return Messages.invalid_username
    if not password_verifier(password):
        return Messages.invalid_password
    if database.is_such_user_in_base(name):
        return Messages.user_is_in_base
    return Messages.all_done


@router.post("/user", response_model=models.ResponseModel)
async def create_user(user: models.CreateUserModel):
    user_info = user.dict()
    log.debug(f"CreateUser request: " + str(user_info))
    name, password = user_info[cnt.NAME], user_info[cnt.PASSWORD]
    database = DataBase()
    response_message = _verify_user_info_in_database(database, name, password)
    if response_message == Messages.all_done:
        database.add_user(name, password)
    response = asdict(response_message)
    log.debug(f"CreateUser response: " + str(response))
    return response


@router.delete("/user", response_model=models.ResponseModel)
async def delete_user(user: models.UserModel):
    user_info = user.dict()
    log.debug(f"DeleteUser request: " + str(user_info))
    database = DataBase()
    delete_users_count = database.delete_user_by_name(user_info[cnt.NAME])
    response_message = Messages.user_not_found if delete_users_count == 0 else Messages.all_done
    response = asdict(response_message)
    log.debug(f"DeleteUser response: " + str(response))
    return response


@router.get("/users")
async def get_users(request: models.TokenModel):
    user_info = request.dict()
    log.debug(f"GetUserList request: " + str(user_info))
    database = DataBase()
    users = database.get_users()
    log.debug(f"GetUserList response: " + str(users))
    return users
