from fastapi.routing import APIRouter
from server import models
from server.database import DataBase
from server import constants as cnt
from server.common import get_response_message
from server.user_manager import generate_user
from server.verifiers import username_verifier
from log import get_file_only_logger

log = get_file_only_logger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


def _verify_user_info_in_database(database: DataBase, name: str, password: str) -> str:
    if not username_verifier.verify(name):
        message_desc = cnt.MSG_INVALID_USERNAME
    elif len(password.strip()) == 0:
        message_desc = cnt.MSG_INVALID_PASSWORD
    elif database.is_such_user_in_base(name):
        message_desc = cnt.MSG_USER_IS_IN_BASE
    else:
        message_desc = cnt.MSG_ALL_DONE
    return message_desc


@router.post("/user", response_model=models.ResponseModel)
async def create_user(user: models.CreateUserModel):
    user_info = user.dict()
    log.debug(f"CreateUser request: " + str(user_info))
    database = DataBase()
    msg_desc = _verify_user_info_in_database(
        database,
        name=user_info[cnt.NAME],
        password=user_info[cnt.PASSWORD]
    )
    if msg_desc == cnt.MSG_ALL_DONE:
        generate_user(user_info)
        database.add_user(user_info[cnt.NAME], user_info[cnt.PASSWORD])
    response = get_response_message(msg_desc)
    log.debug(f"CreateUser response: " + str(response))
    return response


@router.delete("/user", response_model=models.ResponseModel)
async def delete_user(user: models.UserModel):
    user_info = user.dict()
    log.debug(f"DeleteUser request: " + str(user_info))
    database = DataBase()
    delete_users_count = database.delete_user_by_name(user_info[cnt.NAME])
    if delete_users_count == 0:
        response = get_response_message(cnt.MSG_USER_NOT_FOUND)
    else:
        response = get_response_message(cnt.MSG_ALL_DONE)
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
