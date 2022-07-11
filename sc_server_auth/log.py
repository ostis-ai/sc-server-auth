import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

root_dir_path = Path(__file__).resolve().parent
LOG_DIR_PATH = "loggings"
LOG_FILE_NAME = "external-modules.log"
Path(root_dir_path / LOG_DIR_PATH).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[RotatingFileHandler(root_dir_path / LOG_DIR_PATH / LOG_FILE_NAME, maxBytes=1_000_000, backupCount=5)],
)


def get_file_only_logger(name):
    return logging.getLogger(name)


def get_default_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    return logger
