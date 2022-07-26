from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import sc_server_auth.configs.constants as c


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
class GoogleParams:
    secret: str
    scope: str
    local_server_port: int
    token_min_length: int


@dataclass
class ServerParams:
    protocol: str
    host: str
    port: int


class Database(Enum):
    SQLITE = c.SQLITE
    POSTGRES = c.POSTGRES


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
    database: DatabaseParams
    google: GoogleParams


@dataclass
class RunArgs:
    host: str = None
    port: int = None
    database: Database = None
    log_level: str = None
    reload: bool = False
    dot_env: Path = Path(".env")
    google_secret: Path = None
