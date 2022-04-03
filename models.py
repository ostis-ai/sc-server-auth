from typing import Optional
from pydantic import BaseModel
from enum import Enum
from typing import Optional
import jwt
from pydantic.class_validators import validator
from pydantic import BaseModel
from fastapi import HTTPException

import constants as cnt
from config import params

class TokenType(Enum):
    ACCESS = 0
    REFRESH = 1


class Token(BaseModel):
    token: str
    token_type: Optional[str] = None
    expires_in: Optional[str] = None

    @validator("token")
    def validate_token(cls, value):
        try:
            with open(params[cnt.PUBLIC_KEY_PATH], 'rb') as file:
                public_key = file.read()
                jwt.decode(value, public_key,
                        issuer=params[cnt.ISSUER],
                        algorithm='RS256')
        except (jwt.exceptions.InvalidTokenError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.InvalidIssuerError,
                jwt.exceptions.ExpiredSignatureError,
                FileNotFoundError):
            raise HTTPException(status_code=403, detail=params[cnt.MSG_ACCESS_DENIED])
        return value


class Credentials(BaseModel):
    name: str
    password: str

class UserIn(BaseModel):
    access_token: str
    name: str

    @validator("access_token")
    def validate_token(cls, value):
        try:
            with open(params[cnt.PUBLIC_KEY_PATH], 'rb') as file:
                public_key = file.read()
                jwt.decode(value, public_key,
                        issuer=params[cnt.ISSUER],
                        algorithm='RS256')
        except (jwt.exceptions.InvalidTokenError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.InvalidIssuerError,
                jwt.exceptions.ExpiredSignatureError,
                FileNotFoundError):
            raise HTTPException(status_code=403, detail=params[cnt.MSG_ACCESS_DENIED])
        return value


class UserInCreate(UserIn):
    password: str
    role: Optional[str] = None
    lang: Optional[str] = None

   
class Response(BaseModel):
    msg_code: str
    msg_text: Optional[str] = None

class GetTokensResponse(Response):
    access_token: Token
    refresh_token: Token

class GetAccessTokenResponse(Response):
    access_token: Token

