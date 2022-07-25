import time
from os.path import isfile

import jwt
import OpenSSL.crypto as crypto
from fastapi.routing import APIRouter
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

import sc_server_auth.configs.constants as c
import sc_server_auth.server.models as m
from sc_server_auth.configs.log import get_file_only_logger
from sc_server_auth.configs.parser import get_config
from sc_server_auth.configs.paths import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH
from sc_server_auth.server.database import DataBase
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

log = get_file_only_logger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def _generate_token(life_span: m.LifeSpan, username: str) -> bytes:
    generate_keys_if_not_exist()
    with open(PRIVATE_KEY_PATH, "rb") as file:
        private_key = file.read()
    payload = {c.ISS: config.issuer, c.EXP: time.time() + life_span.value, c.USERNAME: username}
    token = jwt.encode(payload, key=private_key, algorithm=c.RS256)
    return token


@router.post("/get_tokens", response_model=m.GetTokensResponseModel)
async def get_tokens(credentials: m.CredentialsModel):
    credentials_dict = credentials.dict()
    log.debug(f"GetTokens request: " + str(credentials_dict))
    database = DataBase()
    username, password = credentials_dict.values()
    log.debug(f"Username: " + str(username))
    if database.is_user_valid(username, password):
        access_token_data = _generate_token(m.LifeSpan.ACCESS, str(username))
        refresh_token_data = _generate_token(m.LifeSpan.REFRESH, str(username))
        response = m.ResponseModels.all_done.dict()
        response.update(
            {
                c.ACCESS_TOKEN: {
                    c.TOKEN: access_token_data.decode(),
                },
                c.REFRESH_TOKEN: {
                    c.TOKEN: refresh_token_data.decode(),
                },
            }
        )
    else:
        response = m.ResponseModels.user_not_found
    log.debug(f"GetTokens response: " + str(response))
    return response


@router.post("/get_access_token", response_model=m.GetAccessTokenResponseModel)
async def get_access_token(token: m.TokenModel):
    generate_keys_if_not_exist()
    with open(PUBLIC_KEY_PATH, "rb") as file:
        public_key = file.read()
    request_params = token.dict()
    log.debug(f"GetAccessToken request: " + str(request_params))
    decoded_data = jwt.decode(request_params[c.TOKEN], public_key, issuer=config.issuer, algorithm=c.RS256)
    username = decoded_data[c.USERNAME]
    log.debug(f"Username: " + username)
    if decoded_data[c.EXP] - time.time() < config.access_token_life_span:
        response = m.ResponseModels.token_expired.dict()
    username = jwt.decode(request_params[cnt.TOKEN], public_key, issuer=params[cnt.ISSUER], algorithm="RS256")[
        cnt.USERNAME
    ]

    ttl = jwt.decode(request_params[cnt.TOKEN], public_key, issuer=params[cnt.ISSUER], algorithm="RS256")[cnt.EXP]

    log.debug(f"Username: " + str(username))

    if ttl - time.time() < params[cnt.ACCESS_TOKEN_LIFE_SPAN]:
        response = get_response_message(cnt.MSG_TOKEN_ERROR)
    else:
        response = m.ResponseModels.all_done.dict()
        response.update(
            {
                c.ACCESS_TOKEN: {
                    c.TOKEN: _generate_token(m.LifeSpan.ACCESS, username).decode(),
                }
            }
        )
    log.debug(f"GetAccessToken response: " + str(response))
    return response


@router.post("/get_google_token", response_model=models.GetAccessTokenResponseModel)
async def get_google_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        params[cnt.GOOGLE_CLIENT_SECRET], ["https://www.googleapis.com/auth/userinfo.profile"]
    )
    creds = flow.run_local_server(port=0)
    creds.refresh(Request())

    response = get_response_message(cnt.MSG_ALL_DONE)
    response.update(
        {
            cnt.ACCESS_TOKEN: {
                cnt.TOKEN: creds.id_token,
            }
        }
    )
    log.debug(f"GetAccessToken response: " + str(response))
    return response
