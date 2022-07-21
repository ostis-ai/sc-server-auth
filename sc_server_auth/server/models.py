from enum import Enum
import json
from typing import Optional

import jwt
from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.dataclasses import dataclass

import sc_server_auth.configs.constants as cnt
from sc_server_auth.configs.parser import get_config
from sc_server_auth.configs.paths import PUBLIC_KEY_PATH
from sc_server_auth.server.keys import generate_keys_if_not_exist

config_tokens = get_config().tokens


class LifeSpan(Enum):
    ACCESS = config_tokens.access_token_life_span
    REFRESH = config_tokens.refresh_token_life_span


class ResponseModel(BaseModel):
    msg_code: str
    msg_text: str


@dataclass(init=False, frozen=True)
class ResponseModels:
    all_done = ResponseModel(msg_code="0", msg_text="All done")
    invalid_username = ResponseModel(msg_code="1", msg_text="User name is incorrect")
    invalid_password = ResponseModel(msg_code="2", msg_text="User password is incorrect")
    user_not_found = ResponseModel(msg_code="3", msg_text="User not found in database")
    user_is_in_base = ResponseModel(msg_code="4", msg_text="User already exists in database")
    sc_server_error = ResponseModel(msg_code="5", msg_text="An error has occurred on sc-server")
    access_denied = ResponseModel(msg_code="6", msg_text="Access denied")
    invalid_request = ResponseModel(msg_code="7", msg_text="Invalid request")
    token_expired = ResponseModel(msg_code="8", msg_text="Token expired")
from sc_server_auth.config import params
from sc_server_auth.server import constants as cnt
from google.oauth2 import id_token
from google.auth.transport import requests


def _validate_google_token(value):
    try:
        with open(params[cnt.GOOGLE_CLIENT_SECRET]) as file:
            client_id = json.loads(file.read())["installed"]["client_id"]
            id_token.verify_oauth2_token(value, requests.Request(), client_id)
    except Exception:
        raise HTTPException(status_code=403, detail=params[cnt.MSG_ACCESS_DENIED])

    return value


def _validate_server_token(value):
    generate_keys_if_not_exist()
    try:
        with open(PUBLIC_KEY_PATH, "rb") as file:
            public_key = file.read()
        jwt.decode(value, public_key, issuer=config_tokens.issuer, algorithm=cnt.RS256)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=403, detail=ResponseModels.access_denied.msg_text)
    return value


def _validate_token(value):
    if len(value) > 800:
        return _validate_google_token(value)
    else:
        return _validate_server_token(value)


class TokenModel(BaseModel):
    token: str

    @validator("token")
    def validate_token(cls, value):
        return _validate_token(value)


class CredentialsModel(BaseModel):
    name: str
    password: str


class UserModel(BaseModel):
    access_token: str
    name: str

    @validator("access_token")
    def validate_token(cls, value):
        return _validate_token(value)


class CreateUserModel(UserModel):
    password: str
    template: str
    args: dict


class GetTokensResponseModel(ResponseModel):
    access_token: TokenModel = None
    refresh_token: TokenModel = None


class GetAccessTokenResponseModel(ResponseModel):
    access_token: TokenModel = None
