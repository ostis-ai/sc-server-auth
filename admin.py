from fastapi.routing import APIRouter
from models import Response, Token, UserIn, UserInCreate
from database import DataBase
import constants as cnt
from common import get_response_message
from verifiers import username_verifier
import requests

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
    print(user_info)
    database = DataBase()
    msg_desc = _verify_user_info_in_database(
            database,
            name=user_info[cnt.NAME],
            password=user_info[cnt.PASSWORD]
            )
    response = get_response_message(msg_desc)
    if msg_desc == cnt.MSG_ALL_DONE:
        database.add_user(user_info[cnt.NAME], user_info[cnt.PASSWORD])
    sc_response = requests.post(url="http://127.0.0.1:8090/admin/user", json=user_info).json()
    print(sc_response)
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

