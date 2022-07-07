from main import app
from fastapi.testclient import TestClient
from config import params, BASE_AUTH_SERVER_URL
from server import constants as cnt
import unittest


class BaseServerTestCase(unittest.TestCase):
    tokens_url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
    access_token_url = BASE_AUTH_SERVER_URL + params[cnt.GET_ACCESS_TOKEN_ENDPOINT]
    user_url = BASE_AUTH_SERVER_URL + params[cnt.USER_ENDPOINT]
    users_url = BASE_AUTH_SERVER_URL + params[cnt.USERS_ENDPOINT]
    test_client = TestClient(app)

    @staticmethod
    def create_user_request(
            token="wrong_token",
            name="Ivan",
            password="Ivan_007",
            template="str",
            args={}):
        return {cnt.ACCESS_TOKEN: token, cnt.NAME: name, cnt.PASSWORD: password, cnt.TEMPLATE: template, cnt.ARGS: args}

    @staticmethod
    def delete_user_request(token="wrong_token", name="Ivan"):
        return {cnt.ACCESS_TOKEN: token, cnt.NAME: name}

    @staticmethod
    def get_tokens_request(
            name="admin",
            password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
    ):
        return {cnt.NAME: name, cnt.PASSWORD: password}

    @staticmethod
    def get_token_request(token="wrong_token"):
        return {cnt.TOKEN: token}

