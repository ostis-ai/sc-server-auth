import sc_server_auth.configs.constants as cnt

# sc_server_params = {
#     cnt.PROTOCOL: "ws://",
#     cnt.HOST: "127.0.0.1",
#     cnt.PORT: ":8090",
#     cnt.WS_JSON_URL: "/ws_json",
#     cnt.TOKEN_QUERY_ARG: "?token=",
#     cnt.SC_CREATE_USER_ENDPOINT: "/admin/user",
# }
#
# BASE_SC_SERVER_URL = (
#     sc_server_params[cnt.PROTOCOL]
#     + sc_server_params[cnt.HOST]
#     + sc_server_params[cnt.PORT]
#     + sc_server_params[cnt.WS_JSON_URL]
# )
#
# TOKEN_SC_SERVER_URL = BASE_SC_SERVER_URL + sc_server_params[cnt.TOKEN_QUERY_ARG]


params = {
    # token params
    cnt.ACCESS_TOKEN_LIFE_SPAN: 1800,
    cnt.REFRESH_TOKEN_LIFE_SPAN: 2592000,
    cnt.BITS: 2048,
    cnt.ISSUER: "sc-auth-server",
    cnt.PROTOCOL: "http://",
    cnt.HOST: "127.0.0.1",
    cnt.PORT: ":5000",
    cnt.GET_TOKENS_ENDPOINT: "/auth/get_tokens",
    cnt.GET_ACCESS_TOKEN_ENDPOINT: "/auth/get_access_token",
    cnt.USER_ENDPOINT: "/admin/user",
    cnt.USERS_ENDPOINT: "/admin/users",
}

BASE_AUTH_SERVER_URL = f"{params[cnt.PROTOCOL]}{params[cnt.HOST]}{params[cnt.PORT]}"
