import logging
from logging.handlers import RotatingFileHandler

from sc_server_auth.configs.parser import get_config
from sc_server_auth.configs.paths import LOG_PATH

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[RotatingFileHandler(LOG_PATH, maxBytes=1_000_000, backupCount=5)],
)


def get_file_only_logger(name):
    return logging.getLogger(name)


def get_default_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(get_config().common.log_level)
    logger.addHandler(logging.StreamHandler())
    return logger
