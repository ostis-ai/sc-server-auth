from main import app
from fastapi.testclient import TestClient
from config import params, BASE_AUTH_SERVER_URL
from server import constants as cnt
import unittest

test_client = TestClient(app)


def create_user_request(token="wrong_token",
                        name="Ivan",
                        password="Ivan_007",
                        template="str",
                        args={}):
    return {"access_token": token, "name": name, "password": password, "template": template, "args": args}


def delete_user_request(token="wrong_token", name="Ivan"):
    return {"access_token": token, "name": name}


def get_tokens(
        name="admin",
        password="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
):
    return {"name": name, "password": password}


def get_token(token="wrong_token"):
    return {"token": token}


get_tokens_url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
get_access_token_url = BASE_AUTH_SERVER_URL + params[cnt.GET_ACCESS_TOKEN_ENDPOINT]
user_url = BASE_AUTH_SERVER_URL + params[cnt.USER_ENDPOINT]
users_url = BASE_AUTH_SERVER_URL + params[cnt.USERS_ENDPOINT]


class BaseServerTestCase(unittest.TestCase):
    pass



