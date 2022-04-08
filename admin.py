from fastapi.routing import APIRouter
from sqlalchemy.sql.traversals import SKIP_TRAVERSE
from json_client.constants import sc_types
from json_client.constants.common import STRING
from json_client.dataclass import ScConstruction, ScIdtfResolveParams, ScLinkContent, ScLinkContentType
from models import Response, Token, UserIn, UserInCreate
from database import DataBase
import constants as cnt
from common import get_response_message
from verifiers import username_verifier
import requests
from config import params
from log import get_default_logger
from json_client import client
from fastapi import Body
from auth import _generate_token, TokenType

log = get_default_logger(__name__)

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


@router.post("/user", response_model=Response)
async def create_user(user: UserInCreate):
    user_info = user.dict()
    log.info(user_info)
    database = DataBase()
    msg_desc = _verify_user_info_in_database(
            database,
            name=user_info[cnt.NAME],
            password=user_info[cnt.PASSWORD]
            )
    response = get_response_message(msg_desc)
    database.add_user(user_info[cnt.NAME], user_info[cnt.PASSWORD])
    generate_user(user_info)
#    response = get_response_message(cnt.MSG_SC_SERVER_ERROR)
    log.info(response)
    return response


@router.delete("/user", response_model=Response)
async def delete_user(user: UserIn):
    user_info = user.dict()
    log.info(user_info)
    database = DataBase()
    delete_users_count = database.delete_user_by_name(user_info[cnt.NAME])
    if delete_users_count == 0:
        response = get_response_message(cnt.MSG_USER_NOT_FOUND)
    else:
        response = get_response_message(cnt.MSG_ALL_DONE)
    log.info(response)
    return response


@router.get("/users")
async def get_users(token: Token):
    database = DataBase()
    users = database.get_users()
    log.info(users)
    return users


def generate_user(user_info: dict):
    client.connect(url=f'{params[cnt.WS_JSON_URL]}{cnt.TOKEN_QUERY_ARG}{_generate_token(TokenType.ACCESS, cnt.AUTH_SERVER).decode()}')
    const = ScConstruction()

    const.create_node(sc_types.NODE_CONST, f'{cnt.MAIN}_{cnt.NODE}')

    rrel_1_params = ScIdtfResolveParams(idtf=cnt.RREL_1, type=sc_types.NODE_CONST_ROLE)
    rrel_2_params = ScIdtfResolveParams(idtf=cnt.RREL_2, type=sc_types.NODE_CONST_ROLE)
    addrs = client.resolve_keynodes([rrel_1_params, rrel_2_params])

    template_link_content = ScLinkContent(user_info[cnt.TEMPLATE], ScLinkContentType.STRING.value)
    const.create_link(sc_types.LINK, template_link_content, f'{cnt.TEMPLATE}_{cnt.LINK}')
    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, f'{cnt.MAIN}_{cnt.NODE}', f'{cnt.TEMPLATE}_{cnt.LINK}', f'{cnt.TEMPLATE}_{cnt.EDGE}')
    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, addrs[0], f'{cnt.TEMPLATE}_{cnt.EDGE}', f'{cnt.RREL_1}_{cnt.EDGE}')

    const.create_node(sc_types.NODE_CONST, f'{cnt.ARGS}_{cnt.NODE}')
    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, f'{cnt.MAIN}_{cnt.NODE}', f'{cnt.ARGS}_{cnt.NODE}', f'{cnt.ARGS}_{cnt.EDGE}')
    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, addrs[1], f'{cnt.ARGS}_{cnt.EDGE}')

    args = user_info[cnt.ARGS]
    args[cnt.LOGIN] = {
        cnt.VALUE: user_info[cnt.NAME],
        cnt.TYPE: cnt.FILE
    }

    for role in args:
        generate_arg_struct(const, role, args[role])
    client.create_elements(const)
    client.disconnect()


def generate_arg_struct(const: ScConstruction, role: str, role_params: dict):
    value_content = ScLinkContent(role_params[cnt.VALUE], ScLinkContentType.STRING.value)
    const.create_link(sc_types.LINK, value_content, f'{cnt.VALUE}_{role}')

    type_params = ScIdtfResolveParams(idtf=role_params[cnt.TYPE], type=None)
    node_type = client.resolve_keynodes([type_params])[0]
    const.create_edge(sc_types.EDGE_D_COMMON_CONST, f'{cnt.VALUE}_{role}', node_type, f'{cnt.EDGE}_{role}')

    role_content = ScLinkContent(role, ScLinkContentType.STRING.value)
    const.create_link(sc_types.LINK, role_content, f'{cnt.ROLE}_{role}')

    const.create_node(sc_types.NODE_CONST, f'{cnt.NODE}_{role}')

    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, f'{cnt.NODE}_{role}', f'{cnt.EDGE}_{role}')

    const.create_edge(sc_types.EDGE_D_COMMON_CONST, f'{cnt.ROLE}_{role}', f'{cnt.NODE}_{role}', f'{cnt.ROLE}_{cnt.EDGE}_{role}')

    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, f'{cnt.ARGS}_{cnt.NODE}', f'{cnt.ROLE}_{cnt.EDGE}_{role}', f'{cnt.ARGS}_{role}_{cnt.EDGE}')
