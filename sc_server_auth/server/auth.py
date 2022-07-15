import time
from dataclasses import asdict

import jwt
import OpenSSL.crypto as crypto
from fastapi.routing import APIRouter

import sc_server_auth.configs.constants as cnt
from sc_server_auth.configs.log import get_file_only_logger
from sc_server_auth.configs.models import Messages, TokenType
from sc_server_auth.configs.parser import get_config
from sc_server_auth.configs.paths import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH
from sc_server_auth.server import models
from sc_server_auth.server.database import DataBase

log = get_file_only_logger(__name__)
config = get_config().tokens

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def _generate_token(token_type: TokenType, username: str) -> bytes:
    if not PRIVATE_KEY_PATH.exists():
        _generate_keys()
    with open(PRIVATE_KEY_PATH, "rb") as file:
        private_key = file.read()
    life_span = config.access_token_life_span if token_type == TokenType.ACCESS else config.refresh_token_life_span
    payload = {cnt.ISS: config.issuer, cnt.EXP: time.time() + life_span, cnt.USERNAME: username}
    token = jwt.encode(payload, key=private_key, algorithm="RS256")
    return token


def _generate_keys() -> None:
    pkey = crypto.PKey()
    pkey.generate_key(type=crypto.TYPE_RSA, bits=config.bits)
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(crypto.dump_publickey(crypto.FILETYPE_PEM, pkey))


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
    try:
        with open(PUBLIC_KEY_PATH, "rb") as file:
            public_key = file.read()
    except FileNotFoundError:
        log.error(Exception(FileNotFoundError))
        raise Exception(FileNotFoundError)
    request_params = token.dict()
    log.debug(f"GetAccessToken request: " + str(request_params))
    username = jwt.decode(request_params[cnt.TOKEN], public_key, issuer=config.issuer, algorithm="RS256")[cnt.USERNAME]

    ttl = jwt.decode(request_params[cnt.TOKEN], public_key, issuer=config.issuer, algorithm="RS256")[cnt.EXP]

    log.debug(f"Username: " + username)

    if ttl - time.time() < config.access_token_life_span:
        response = asdict(Messages.token_expired)
    else:
        access_token_data = _generate_token(TokenType.ACCESS, username)
        response = asdict(Messages.all_done)
        response.update(
            {
                cnt.ACCESS_TOKEN: {
                    cnt.TOKEN: access_token_data.decode(),
                }
            }
        )
    log.debug(f"GetAccessToken response: " + str(response))
    return response
