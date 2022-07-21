import json
from typing import Optional

import jwt
from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel
from pydantic.class_validators import validator

from sc_server_auth.config import params
from sc_server_auth.server import constants as cnt


def _validate_google_token(value):
    try:
        with open(params[cnt.GOOGLE_CLIENT_SECRET]) as file:
            client_id = json.loads(file.read())["installed"]["client_id"]
            id_token.verify_oauth2_token(value, requests.Request(), client_id)
    except Exception:
        raise HTTPException(status_code=403, detail=params[cnt.MSG_ACCESS_DENIED])

    return value


def _validate_server_token(value):
    try:
        with open(params[cnt.PUBLIC_KEY_PATH], "rb") as file:
            public_key = file.read()
            jwt.decode(value, public_key, issuer=params[cnt.ISSUER], algorithm="RS256")
    except (
        jwt.exceptions.InvalidTokenError,
        jwt.exceptions.InvalidSignatureError,
        jwt.exceptions.InvalidIssuerError,
        jwt.exceptions.ExpiredSignatureError,
        FileNotFoundError,
    ):
        raise HTTPException(status_code=403, detail=params[cnt.MSG_ACCESS_DENIED])
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


class ResponseModel(BaseModel):
    msg_code: str
    msg_text: Optional[str] = None


class GetTokensResponseModel(ResponseModel):
    access_token: TokenModel = None
    refresh_token: TokenModel = None


class GetAccessTokenResponseModel(ResponseModel):
    access_token: TokenModel = None
