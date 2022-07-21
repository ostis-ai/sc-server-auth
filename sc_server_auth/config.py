from enum import Enum

from sc_server_auth.server import constants as cnt


class TokenType(Enum):
    ACCESS = 0
    REFRESH = 1


sc_server_params = {
    cnt.PROTOCOL: "ws://",
    cnt.HOST: "127.0.0.1",
    cnt.PORT: ":8090",
    cnt.WS_JSON_URL: "/ws_json",
    cnt.TOKEN_QUERY_ARG: "?token=",
    cnt.SC_CREATE_USER_ENDPOINT: "/admin/user",
}

BASE_SC_SERVER_URL = (
    sc_server_params[cnt.PROTOCOL]
    + sc_server_params[cnt.HOST]
    + sc_server_params[cnt.PORT]
    + sc_server_params[cnt.WS_JSON_URL]
)

TOKEN_SC_SERVER_URL = BASE_SC_SERVER_URL + sc_server_params[cnt.TOKEN_QUERY_ARG]


params = {
    # path params
    cnt.SQLITE_DB_PATH: "sqlite:///" + "database.db",
    cnt.PRIVATE_KEY_PATH: "private.pem",
    cnt.PUBLIC_KEY_PATH: "public.pem",
    cnt.GOOGLE_CLIENT_SECRET: "sc_server_auth/client_secret.json",
    # validator patters
    cnt.USERNAME_PATTERN: r"^[a-zA-Z][a-zA-Z0-9-_.]{1,20}$",
    cnt.PASSWORD_PATTERN: r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&-_]{6,}$",
    # token params
    cnt.ACCESS_TOKEN_LIFE_SPAN: 1800,
    cnt.REFRESH_TOKEN_LIFE_SPAN: 2_593_800,
    cnt.BITS: 2048,
    cnt.ISSUER: "sc-auth-server",
    cnt.PROTOCOL: "http://",
    cnt.HOST: "127.0.0.1",
    cnt.PORT: ":5000",
    cnt.GET_TOKENS_ENDPOINT: "/auth/get_tokens",
    cnt.GET_ACCESS_TOKEN_ENDPOINT: "/auth/get_access_token",
    cnt.USER_ENDPOINT: "/admin/user",
    cnt.USERS_ENDPOINT: "/admin/users",
    # messages
    cnt.MSG_ACCESS_DENIED: "Access denied",
    cnt.MSG_INVALID_REQUEST: "Invalid request",
    # message codes
    cnt.MSG_CODES: {
        cnt.MSG_ALL_DONE: 0,
        cnt.MSG_INVALID_USERNAME: 1,
        cnt.MSG_INVALID_PASSWORD: 2,
        cnt.MSG_USER_NOT_FOUND: 3,
        cnt.MSG_USER_IS_IN_BASE: 4,
        cnt.MSG_SC_SERVER_ERROR: 5,
        cnt.MSG_TOKEN_ERROR: 6,
    },
    # messages text
    cnt.MSG_TEXT: {
        cnt.MSG_ALL_DONE: "All done",
        cnt.MSG_INVALID_USERNAME: "User name is incorrect",
        cnt.MSG_INVALID_PASSWORD: "User password is incorrect",
        cnt.MSG_USER_NOT_FOUND: "User not found in database",
        cnt.MSG_USER_IS_IN_BASE: "User already exists in database",
        cnt.MSG_SC_SERVER_ERROR: "An error has occurred on sc-server",
        cnt.MSG_TOKEN_ERROR: "Token expired",
    },
}

BASE_AUTH_SERVER_URL = params[cnt.PROTOCOL] + params[cnt.HOST] + params[cnt.PORT]
