import unittest
import requests
from config import params, BASE_AUTH_SERVER_URL
from server import constants as cnt

user_creds = {"name": "admin", "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_user_creds = {"name": "stas", "password": "a665a45923422f9d417e5867efdc4fb8a06a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_pass_creds = {"name": "admin", "password": "a665a45923422f9d417e5867efdc4fb8a06a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_token = {"token": "wrong_token"}


class ServerTest(unittest.TestCase):
    def test_get_tokens(self):
        url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
        response = requests.post(url=url, json=user_creds).json()
        self.assertEqual(int(response['msg_code']), 0)
        self.assertTrue(response['access_token'])
        self.assertTrue(response['refresh_token'])

    def test_get_tokens_no_user_in_db(self):
        url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
        response = requests.post(url=url, json=wrong_user_creds).json()
        self.assertEqual(int(response['msg_code']), params[cnt.MSG_CODES][cnt.MSG_USER_NOT_FOUND])

    def test_get_tokens_empty(self):
        url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
        response = requests.post(url=url).status_code
        self.assertEqual(response, 422)

    def test_get_access_token(self):
        refresh_token_url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
        refresh_token = requests.post(url=refresh_token_url, json=user_creds).json()['refresh_token']['token']
        access_token_url = BASE_AUTH_SERVER_URL + params[cnt.GET_ACCESS_TOKEN_ENDPOINT]
        response = requests.post(url=access_token_url, json={'token': refresh_token}).json()
        self.assertEqual(response['msg_code'], '0')
        self.assertTrue(response['access_token'])

    def test_get_access_token_wrong(self):
        url = BASE_AUTH_SERVER_URL + params[cnt.GET_ACCESS_TOKEN_ENDPOINT]
        response = requests.post(url=url, json=wrong_token).status_code
        self.assertEqual(response, 403)


if __name__ == '__main__':
    unittest.main()
