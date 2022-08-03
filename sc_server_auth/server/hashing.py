import hashlib

from sc_server_auth.configs.parser import get_config

config = get_config().hashing


def hash_password(password: str) -> str:
    enc = hashlib.pbkdf2_hmac(config.name, password.encode(), config.salt, config.iters)
    return enc.hex()


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
