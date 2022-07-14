import sc_server_auth.configs.constants as cnt
from sc_server_auth.configs.params import params


def get_response_message(message_desc: str) -> dict:
    response = {
        cnt.MSG_CODE: params[cnt.MSG_CODES][message_desc],
        cnt.MSG_TEXT: params[cnt.MSG_TEXT][message_desc],
    }
    return response
