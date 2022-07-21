from dataclasses import dataclass
from enum import Enum, IntEnum
from pathlib import Path


class TokenType(IntEnum):
    ACCESS = 0
    REFRESH = 1


@dataclass
class Message:
    msg_code: int
    msg_text: str


@dataclass(frozen=True)
class Messages:
    all_done = Message(0, "All done")
    invalid_username = Message(1, "User name is incorrect")
    invalid_password = Message(2, "User password is incorrect")
    user_not_found = Message(3, "User not found in database")
    user_is_in_base = Message(4, "User already exists in database")
    sc_server_error = Message(5, "An error has occurred on sc-server")
    access_denied = Message(6, "Access denied")
    invalid_request = Message(7, "Invalid request")
    token_expired = Message(8, "Token expired")


@dataclass
class CommonParams:
    log_level: str


@dataclass
class TokensParams:
    access_token_life_span: int
    refresh_token_life_span: int
    bits: int
    issuer: str


@dataclass
class ServerParams:
    protocol: str
    host: str
    port: int


# @dataclass
# class ScServerParams(ServerParams):
#     ws_json_url: str
#     sc_create_user_endpoint: str


class Database(Enum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"


class IsolationLevel(Enum):
    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"


@dataclass
class DatabaseParams:
    database: Database
    user: str
    password: str
    name: str
    host: str
    isolation_level: IsolationLevel


@dataclass
class Config:
    common: CommonParams
    tokens: TokensParams
    server: ServerParams
    # sc_server: ScServerParams
    database: DatabaseParams


@dataclass
class RunArgs:
    host: str = None
    port: int = None
    database: Database = None
    log_level: str = None
    reload: bool = False
    dot_env: Path = None
