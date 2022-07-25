from fastapi.routing import APIRouter

import sc_server_auth.configs.constants as c
import sc_server_auth.server.models as m
from sc_server_auth.configs.log import get_file_only_logger
from sc_server_auth.server.database import DataBase
from sc_server_auth.server.verifiers import password_verifier, username_verifier

log = get_file_only_logger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


def _verify_user_info_in_database(database: DataBase, name: str, password: str) -> m.ResponseModel:
    if not username_verifier(name):
        return m.ResponseModels.invalid_username
    if not password_verifier(password):
        return m.ResponseModels.invalid_password
    if database.is_such_user_in_base(name):
        return m.ResponseModels.user_is_in_base
    return m.ResponseModels.all_done


@router.post("/user", response_model=m.ResponseModel)
async def create_user(user: m.CreateUserModel):
    user_info = user.dict()
    log.debug(f"CreateUser request: " + str(user_info))
    name, password = user_info[c.NAME], user_info[c.PASSWORD]
    database = DataBase()
    response_model = _verify_user_info_in_database(database, name, password)
    if response_model == m.ResponseModels.all_done:
        database.add_user(name, password)
    response = response_model.dict()
    log.debug(f"CreateUser response: " + str(response))
    return response


@router.delete("/user", response_model=m.ResponseModel)
async def delete_user(user: m.UserModel):
    user_info = user.dict()
    log.debug(f"DeleteUser request: " + str(user_info))
    database = DataBase()
    delete_users_count = database.delete_user_by_name(user_info[c.NAME])
    response_model = m.ResponseModels.user_not_found if delete_users_count == 0 else m.ResponseModels.all_done
    response = response_model.dict()
    log.debug(f"DeleteUser response: " + str(response))
    return response


@router.get("/users")
async def get_users(request: m.TokenModel):
    user_info = request.dict()
    log.debug(f"GetUserList request: " + str(user_info))
    database = DataBase()
    users = database.get_users()
    log.debug(f"GetUserList response: " + str(users))
    return users
