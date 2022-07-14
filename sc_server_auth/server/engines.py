from sqlalchemy import create_engine

from sc_server_auth.configs.models import Database, DatabaseParams
from sc_server_auth.configs.paths import SQLITE_PATH


def create_engine_sqlite():
    return create_engine(f"sqlite:///{SQLITE_PATH}")


def create_engine_postgres():
    return create_engine(
        f"postgresql://{DatabaseParams.user}:{DatabaseParams.password}@{DatabaseParams.host}/{DatabaseParams.name}",
        execution_options={"isolation_level": DatabaseParams.isolation_level.value},
    )


db_engines = {
    Database.SQLITE.value: create_engine_sqlite,
    Database.POSTGRES.value: create_engine_postgres,
}
