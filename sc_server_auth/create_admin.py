from argparse import ArgumentParser
from dataclasses import dataclass
from getpass import getpass

from sc_server_auth.configs.log import get_default_logger
from sc_server_auth.configs.models import Database as DatabaseType
from sc_server_auth.configs.parser import get_config
from sc_server_auth.server.admin import verify_user_info_in_database
from sc_server_auth.server.database import DataBase
from sc_server_auth.server.hashing import hash_password
from sc_server_auth.server.models import ResponseModels

logger = get_default_logger(__name__)


@dataclass
class CreateAdminArgs:
    database: DatabaseType = None
    name: str = None
    password: str = None


def main():
    config_database = get_config().database
    args = CreateAdminArgs()

    parser = ArgumentParser(prog="python -m sc_server_auth.create_admin", description="Create admin and add to db")
    parser.add_argument(
        "-d", "--database", help=f"Database system (default: {config_database.database.value})", type=DatabaseType
    )
    parser.add_argument("-n", "-l", "--name", "--login", type=str)
    parser.add_argument("-p", "--password", type=str)

    parser.parse_args(namespace=args)
    if args.database is not None:
        config_database.database = args.database
        logger.info("Set %s database", args.database.value)
    if args.name is None:
        args.name = input("Enter name: ")
    if args.password is None:
        args.password = getpass("Enter password: ")

    database = DataBase()
    response_model = verify_user_info_in_database(database, args.name, args.password)
    if response_model == ResponseModels.all_done:
        database.add_user(args.name, hash_password(args.password))
        logger.info("Created user '%s'", args.name)
    else:
        logger.info(response_model.msg_text)


if __name__ == "__main__":
    main()
