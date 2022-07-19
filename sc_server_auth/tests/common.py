import unittest

from fastapi.testclient import TestClient

import sc_server_auth.configs.constants as cnt
from sc_server_auth.configs.parser import get_config
from sc_server_auth.main import app

config = get_config()


class BaseServerTestCase(unittest.TestCase):
    base_url = f"{config.server.protocol}{config.server.host}:{config.server.port}"
    tokens_url = f"{base_url}/auth/get_tokens"
    access_token_url = f"{base_url}/auth/get_access_token"
    user_url = f"{base_url}/admin/user"
    users_url = f"{base_url}/admin/users"
    test_client = TestClient(app)

    @staticmethod
    def create_user_request(token="wrong_token", name="Ivan", password="Ivan_007", template="str", args={}):
        return {cnt.ACCESS_TOKEN: token, cnt.NAME: name, cnt.PASSWORD: password, cnt.TEMPLATE: template, cnt.ARGS: args}

    @staticmethod
    def delete_user_request(token="wrong_token", name="Ivan"):
        return {cnt.ACCESS_TOKEN: token, cnt.NAME: name}

    @staticmethod
    def get_tokens_request(name="admin", password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"):
        return {cnt.NAME: name, cnt.PASSWORD: password}

    @staticmethod
    def get_token_request(token="wrong_token"):
        return {cnt.TOKEN: token}
