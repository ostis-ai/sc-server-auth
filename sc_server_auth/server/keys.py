from OpenSSL import crypto

from sc_server_auth.configs.parser import get_config
from sc_server_auth.configs.paths import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH


def _generate_keys() -> None:
    pkey = crypto.PKey()
    pkey.generate_key(type=crypto.TYPE_RSA, bits=get_config().tokens.bits)
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(crypto.dump_publickey(crypto.FILETYPE_PEM, pkey))


def generate_keys_if_not_exist() -> None:
    if not PRIVATE_KEY_PATH.exists() or not PUBLIC_KEY_PATH.exists():
        _generate_keys()
