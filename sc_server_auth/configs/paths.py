from pathlib import Path

CONFIG_DIR_PATH = Path(__file__).resolve().parent
DEV_CONFIG_PATH = CONFIG_DIR_PATH.joinpath("settings.toml")

ROOT_DIR_PATH = CONFIG_DIR_PATH.parent

PRIVATE_KEY_PATH = ROOT_DIR_PATH.joinpath("private.pem")
PUBLIC_KEY_PATH = ROOT_DIR_PATH.joinpath("public.pem")

LOG_DIR_PATH = ROOT_DIR_PATH.joinpath("loggings")
LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_DIR_PATH.joinpath("external-modules.log")

SQLITE_PATH = ROOT_DIR_PATH.parent.joinpath("database.db")
