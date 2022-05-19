import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

root_dir_path = Path(__file__).resolve().parent
log_dir_path = "loggings"
log_file_name = "external-modules.log"
Path(root_dir_path / log_dir_path).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[RotatingFileHandler(root_dir_path / log_dir_path / log_file_name, maxBytes=1_000_000, backupCount=5)],
)


def get_file_only_logger(name):
    return logging.getLogger(name)


def get_default_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    return logger
