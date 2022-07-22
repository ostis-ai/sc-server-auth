import time
from dataclasses import asdict

import jwt
from fastapi.routing import APIRouter

import sc_server_auth.configs.constants as cnt
from sc_server_auth.configs.log import get_file_only_logger
from sc_server_auth.configs.models import Messages, TokenType
from sc_server_auth.configs.parser import get_config
from sc_server_auth.configs.paths import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH
from sc_server_auth.server import models
from sc_server_auth.server.database import DataBase
from sc_server_auth.server.keys import generate_keys_if_not_exist

log = get_file_only_logger(__name__)
config = get_config().tokens

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def _generate_token(token_type: TokenType, username: str) -> bytes:
    generate_keys_if_not_exist()
    with open(PRIVATE_KEY_PATH, "rb") as file:
        private_key = file.read()
    life_span = config.access_token_life_span if token_type == TokenType.ACCESS else config.refresh_token_life_span
    payload = {cnt.ISS: config.issuer, cnt.EXP: time.time() + life_span, cnt.USERNAME: username}
    token = jwt.encode(payload, key=private_key, algorithm=cnt.RS256)
    return token


@router.post("/get_tokens", response_model=models.GetTokensResponseModel)
async def get_tokens(credentials: models.CredentialsModel):
    credentials_dict = credentials.dict()
    log.debug(f"GetTokens request: " + str(credentials_dict))
    database = DataBase()
    username, password = credentials_dict.values()
    log.debug(f"Username: " + str(username))
    if database.is_user_valid(username, password):
        access_token_data = _generate_token(TokenType.ACCESS, str(username))
        refresh_token_data = _generate_token(TokenType.REFRESH, str(username))
        response = asdict(Messages.all_done)
        response.update(
            {
                cnt.ACCESS_TOKEN: {
                    cnt.TOKEN: access_token_data.decode(),
                },
                cnt.REFRESH_TOKEN: {
                    cnt.TOKEN: refresh_token_data.decode(),
                },
            }
        )
    else:
        response = Messages.user_not_found
    log.debug(f"GetTokens response: " + str(response))
    return response


@router.post("/get_access_token", response_model=models.GetAccessTokenResponseModel)
async def get_access_token(token: models.TokenModel):
    generate_keys_if_not_exist()
    with open(PUBLIC_KEY_PATH, "rb") as file:
        public_key = file.read()
    request_params = token.dict()
    log.debug(f"GetAccessToken request: " + str(request_params))
    decoded_data = jwt.decode(request_params[cnt.TOKEN], public_key, issuer=config.issuer, algorithm=cnt.RS256)
    username = decoded_data[cnt.USERNAME]
    log.debug(f"Username: " + username)
    if decoded_data[cnt.EXP] - time.time() < config.access_token_life_span:
        response = asdict(Messages.token_expired)
    else:
        response = asdict(Messages.all_done)
        response.update(
            {
                cnt.ACCESS_TOKEN: {
                    cnt.TOKEN: _generate_token(TokenType.ACCESS, username).decode(),
                }
            }
        )
    log.debug(f"GetAccessToken response: " + str(response))
    return response
