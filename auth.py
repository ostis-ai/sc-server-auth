from fastapi.routing import APIRouter
from models import Credentials, Token, TokenType, GetAccessTokenResponse
import constants as cnt
import jwt
import time
import OpenSSL.crypto as crypto
from config import params
from database import DataBase
from os.path import isfile
from common import get_response_message

router = APIRouter(
        prefix="/auth",
        tags=["auth"],
)

def _generate_token(token_type: TokenType, username: str) -> bytes:
    if not isfile(params[cnt.PRIVATE_KEY_PATH]):
        _generate_keys()
    with open(params[cnt.PRIVATE_KEY_PATH], 'rb') as file:
        private_key = file.read()
    access_token_life_span = params[cnt.ACCESS_TOKEN_LIFE_SPAN]
    refresh_token_life_span = params[cnt.REFRESH_TOKEN_LIFE_SPAN]
    life_span = access_token_life_span if token_type == TokenType.ACCESS else refresh_token_life_span
    payload = {
        cnt.ISS: params[cnt.ISSUER],
        cnt.EXP: time.time() + life_span,
        cnt.USERNAME: username
    }
    token = jwt.encode(payload, key=private_key, algorithm='RS256')
    return token

def _generate_keys() -> None:
    pkey= crypto.PKey()
    pkey.generate_key(type=crypto.TYPE_RSA, bits=params[cnt.BITS])
    with open(params[cnt.PRIVATE_KEY_PATH], "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
    with open(params[cnt.PUBLIC_KEY_PATH], "wb") as f:
        f.write(crypto.dump_publickey(crypto.FILETYPE_PEM, pkey))

@router.post("/get_tokens")
async def get_tokens(credentials: Credentials):
        credentials_dict = credentials.dict()
        database = DataBase()
        username, password = credentials_dict.values()
        if database.is_user_valid(username, password):
            access_token_data = _generate_token(TokenType.ACCESS, str(username))
            refresh_token_data = _generate_token(TokenType.REFRESH, str(username))
            response = {
                cnt.MSG_CODE: params[cnt.MSG_CODES][cnt.MSG_ALL_DONE],
                cnt.ACCESS_TOKEN: {
                    cnt.TOKEN: access_token_data.decode(),
                    cnt.TOKEN_TYPE: cnt.JWT,
                    cnt.EXPIRES_IN: params[cnt.ACCESS_TOKEN_LIFE_SPAN],
                },
                cnt.REFRESH_TOKEN: {
                    cnt.TOKEN: refresh_token_data.decode(),
                    cnt.TOKEN_TYPE: cnt.JWT,
                    cnt.EXPIRES_IN: params[cnt.REFRESH_TOKEN_LIFE_SPAN],
                }
            }
        else:
            response = get_response_message(cnt.MSG_USER_NOT_FOUND)
        return response

@router.post("/get_access_token", response_model=GetAccessTokenResponse)
async def get_access_token(token: Token):
        try:
            with open(params[cnt.PUBLIC_KEY_PATH], 'rb') as file:
                    public_key = file.read()
        except FileNotFoundError:
            raise Exception(FileNotFoundError)
        request_params = token.dict()
        username = jwt.decode(request_params[cnt.TOKEN], public_key,
            issuer=params[cnt.ISSUER],
            algorithm='RS256')[cnt.USERNAME]
        access_token_data = _generate_token(TokenType.ACCESS, username)
        response = {
            cnt.MSG_CODE: params[cnt.MSG_CODES][cnt.MSG_ALL_DONE],
            cnt.ACCESS_TOKEN:{
                cnt.TOKEN: access_token_data.decode(),
                cnt.TOKEN_TYPE: cnt.JWT,
                cnt.EXPIRES_IN: params[cnt.ACCESS_TOKEN_LIFE_SPAN],
            }
        }
        return response
