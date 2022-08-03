import hashlib

_HASH_NAME = "sha256"
_SALT = b"\xf2\x0fr{\x98\x12\x9f\x08'\xfd_\x1f-sF\x84"
_HASH_ITERS = 100_000


def hash_password(password: str) -> str:
    enc = hashlib.pbkdf2_hmac(_HASH_NAME, password.encode(), _SALT, _HASH_ITERS)
    return enc.hex()


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
