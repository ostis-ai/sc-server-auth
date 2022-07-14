from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    ACCESS = 0
    REFRESH = 1


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
    database: Database = Database.SQLITE  # Change database here
    user: str = "sc_auth"
    password: str = "sc_auth"
    name: str = "sc_auth"
    host: str = "localhost"
    isolation_level: IsolationLevel = IsolationLevel.READ_UNCOMMITTED
    # TODO: parse it


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
