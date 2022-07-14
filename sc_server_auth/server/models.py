from typing import Optional

import jwt
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic.class_validators import validator

import sc_server_auth.configs.constants as cnt
from sc_server_auth.configs.models import Messages
from sc_server_auth.configs.params import params
from sc_server_auth.configs.paths import PUBLIC_KEY_PATH


def _validate_token(value):
    try:
        with open(PUBLIC_KEY_PATH, "rb") as file:
            public_key = file.read()
            jwt.decode(value, public_key, issuer=params[cnt.ISSUER], algorithm="RS256")
    except (
        jwt.exceptions.InvalidTokenError,
        jwt.exceptions.InvalidSignatureError,
        jwt.exceptions.InvalidIssuerError,
        jwt.exceptions.ExpiredSignatureError,
        FileNotFoundError,
    ):
        raise HTTPException(status_code=403, detail=Messages.access_denied.msg_text)
    return value


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
