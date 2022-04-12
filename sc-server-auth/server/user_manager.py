from json_client.constants import sc_types
from json_client.dataclass import ScConstruction, ScIdtfResolveParams, ScLinkContent, ScLinkContentType
from json_client import client
from server.auth import _generate_token
from config import TokenType, TOKEN_SC_SERVER_URL
from server import constants as cnt
from functools import wraps


def need_sc_client_connection(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _generate_token(TokenType.ACCESS, cnt.AUTH_SERVER).decode()
        client.connect(TOKEN_SC_SERVER_URL + token)
        if client.is_connected():
            f(*args, **kwargs)
            client.disconnect()
    return decorated


@need_sc_client_connection
def generate_user(user_info: dict):
    const = ScConstruction()
    const.create_node(sc_types.NODE_CONST, f'{cnt.MAIN}_{cnt.NODE}')

    rrel_1_params = ScIdtfResolveParams(idtf=cnt.RREL_1, type=sc_types.NODE_CONST_ROLE)
    rrel_2_params = ScIdtfResolveParams(idtf=cnt.RREL_2, type=sc_types.NODE_CONST_ROLE)
    addrs = client.resolve_keynodes([rrel_1_params, rrel_2_params])

    template_link_content = ScLinkContent(user_info[cnt.TEMPLATE], ScLinkContentType.STRING.value)
    const.create_link(sc_types.LINK, template_link_content, f'{cnt.TEMPLATE}_{cnt.LINK}')
    const.create_edge(
        sc_types.EDGE_ACCESS_CONST_POS_PERM,
        f'{cnt.MAIN}_{cnt.NODE}',
        f'{cnt.TEMPLATE}_{cnt.LINK}',
        f'{cnt.TEMPLATE}_{cnt.EDGE}'
    )
    const.create_edge(
        sc_types.EDGE_ACCESS_CONST_POS_PERM,
        addrs[0],
        f'{cnt.TEMPLATE}_{cnt.EDGE}',
        f'{cnt.RREL_1}_{cnt.EDGE}'
    )

    const.create_node(sc_types.NODE_CONST, f'{cnt.ARGS}_{cnt.NODE}')
    const.create_edge(
        sc_types.EDGE_ACCESS_CONST_POS_PERM,
        f'{cnt.MAIN}_{cnt.NODE}',
        f'{cnt.ARGS}_{cnt.NODE}',
        f'{cnt.ARGS}_{cnt.EDGE}'
    )
    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, addrs[1], f'{cnt.ARGS}_{cnt.EDGE}')

    args = user_info[cnt.ARGS]
    args[cnt.LOGIN] = {
        cnt.VALUE: user_info[cnt.NAME],
        cnt.TYPE: cnt.FILE
    }

    for role in args:
        _generate_arg_struct(const, role, args[role])
    client.create_elements(const)


def _generate_arg_struct(const: ScConstruction, role: str, role_params: dict):
    value_content = ScLinkContent(role_params[cnt.VALUE], ScLinkContentType.STRING.value)
    const.create_link(sc_types.LINK, value_content, f'{cnt.VALUE}_{role}')

    type_params = ScIdtfResolveParams(idtf=role_params[cnt.TYPE], type=None)
    node_type = client.resolve_keynodes([type_params])[0]
    const.create_edge(sc_types.EDGE_D_COMMON_CONST, f'{cnt.VALUE}_{role}', node_type, f'{cnt.EDGE}_{role}')

    role_content = ScLinkContent(role, ScLinkContentType.STRING.value)
    const.create_link(sc_types.LINK, role_content, f'{cnt.ROLE}_{role}')

    const.create_node(sc_types.NODE_CONST, f'{cnt.NODE}_{role}')

    const.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, f'{cnt.NODE}_{role}', f'{cnt.EDGE}_{role}')

    const.create_edge(
        sc_types.EDGE_D_COMMON_CONST,
        f'{cnt.ROLE}_{role}',
        f'{cnt.NODE}_{role}',
        f'{cnt.ROLE}_{cnt.EDGE}_{role}'
    )
    const.create_edge(
        sc_types.EDGE_ACCESS_CONST_POS_PERM,
        f'{cnt.ARGS}_{cnt.NODE}',
        f'{cnt.ROLE}_{cnt.EDGE}_{role}',
        f'{cnt.ARGS}_{role}_{cnt.EDGE}'
    )
