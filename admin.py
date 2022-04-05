from fastapi.routing import APIRouter
from models import Response, Token, UserIn, UserInCreate
from database import DataBase
import constants as cnt
from common import get_response_message
from verifiers import username_verifier
import requests
from config import params

router = APIRouter(
        prefix="/admin",
        tags = ["admin"],
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


@router.post("/user", response_model=Response)
async def create_user(user: UserInCreate):
    user_info = user.dict()
    database = DataBase()
    msg_desc = _verify_user_info_in_database(
            database,
            name=user_info[cnt.NAME],
            password=user_info[cnt.PASSWORD]
            )
    response = get_response_message(msg_desc)
    if msg_desc == cnt.MSG_ALL_DONE:
        sc_response = requests.post(url=params[cnt.SC_SERVER_URL]+params[cnt.SC_CREATE_USER_ENDPOINT], json=user_info).json()
        print(sc_response)
        if sc_response[cnt.MSG_CODE] == params[cnt.MSG_CODES][cnt.MSG_ALL_DONE]:
            database.add_user(user_info[cnt.NAME], user_info[cnt.PASSWORD])
        else:
            response = get_response_message(cnt.MSG_SC_SERVER_ERROR)
    return response

@router.delete("/user", response_model=Response)
async def delete_user(user: UserIn):
    user_info = user.dict()
    database = DataBase()
    delete_users_count = database.delete_user_by_name(user_info[cnt.NAME])
    if delete_users_count == 0:
        response = get_response_message(cnt.MSG_USER_NOT_FOUND)
    else:
        response = get_response_message(cnt.MSG_ALL_DONE)
    return response


@router.get("/users")
async def get_users(token: Token):
    database = DataBase()
    users = database.get_users()
    return users

