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
