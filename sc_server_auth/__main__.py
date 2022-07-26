from argparse import ArgumentParser
from pathlib import Path

import uvicorn

from sc_server_auth.configs.models import Database, RunArgs
from sc_server_auth.configs.parser import Parser, get_config


def main():
    config = get_config()
    args = RunArgs()

    parser = ArgumentParser(prog="python3 -m sc_server_auth", description="Run auth-server application")
    parser.add_argument("-H", "--host", help=f"Bind host (default: {config.server.host})", type=str)
    parser.add_argument("-p", "--port", help=f"Bind port (default: {config.server.port})", type=int)
    parser.add_argument(
        "-d", "--database", help=f"Database system (default: {config.database.database.value})", type=Database
    )
    parser.add_argument("-l", "--log-level", help=f"Logging level (default: {config.common.log_level})", type=str)
    parser.add_argument("-r", "--reload", help="Reload server at changes", action="store_true")
    parser.add_argument("-e", "--dot-env", help=f"*.env file (default: {args.dot_env})", type=Path)
    parser.add_argument(
        "-g", "--google-secret", help=f"Path to google client secret (default: {args.google_secret})", type=Path
    )

    parser.parse_args(namespace=args)
    Parser.set_config_args(args)
    config = Parser.get_config()

    uvicorn.run(app="sc_server_auth.main:app", host=config.server.host, port=config.server.port, reload=args.reload)


if __name__ == "__main__":
    main()
