from argparse import ArgumentParser

import uvicorn

from sc_server_auth.configs.models import Database
from sc_server_auth.configs.parser import get_config


def main():
    config = get_config()

    parser = ArgumentParser(prog="python3 -m sc_server_auth", description="Run SC Server")
    parser.add_argument("-H", "--host", help=f"Bind host  [default: {config.server.host}]", type=str)
    parser.add_argument("-P", "--port", help=f"Bind port  [default: {config.server.port}]", type=int)
    parser.add_argument(
        "-d", "--database", help=f"Database system  [default: {config.database.database.value}]", type=Database
    )
    parser.add_argument("-l", "--log-level", help=f"Logging level  [default: {config.common.log_level}]", type=str)
    parser.parse_args(namespace=config.server)
    parser.parse_args(namespace=config.database)
    parser.parse_args(namespace=config.common)

    uvicorn.run(app="main:app", host=config.server.host, port=config.server.port, reload=True)


if __name__ == "__main__":
    main()
