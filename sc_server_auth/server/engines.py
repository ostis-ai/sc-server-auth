from sqlalchemy import create_engine

from sc_server_auth.configs.models import Database
from sc_server_auth.configs.parser import get_config
from sc_server_auth.configs.paths import SQLITE_PATH

config = get_config().database


def create_engine_sqlite():
    return create_engine(f"sqlite:///{SQLITE_PATH}")


def create_engine_postgres():
    return create_engine(
        f"postgresql://{config.user}:{config.password}@{config.host}/{config.name}",
        execution_options={"isolation_level": config.isolation_level.value},
    )


db_engines = {
    Database.SQLITE.value: create_engine_sqlite,
    Database.POSTGRES.value: create_engine_postgres,
}
