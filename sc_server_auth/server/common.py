from sc_server_auth.config import params
from sc_server_auth.server import constants as cnt


def get_response_message(message_desc: str) -> dict:
    response = {
        cnt.MSG_CODE: params[cnt.MSG_CODES][message_desc],
        cnt.MSG_TEXT: params[cnt.MSG_TEXT][message_desc],
    }
    return response
