from tests.common import *
from config import params, BASE_AUTH_SERVER_URL
from server import constants as cnt


class ServerTest(BaseServerTestCase):
    def test_get_tokens(self):
        url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
        response = test_client.post(url=url, json=get_tokens()).json()

        self.assertEqual(int(response[cnt.MSG_CODE]), params[cnt.MSG_CODES][cnt.MSG_ALL_DONE])
        self.assertTrue(response[cnt.ACCESS_TOKEN])
        self.assertTrue(response[cnt.REFRESH_TOKEN])

    def test_get_tokens_no_user_in_db(self):
        url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
        response = test_client.post(url=url, json=get_tokens(name="Stas")).json()
        self.assertEqual(int(response[cnt.MSG_CODE]), params[cnt.MSG_CODES][cnt.MSG_USER_NOT_FOUND])

    def test_get_tokens_empty(self):
        url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
        response = test_client.post(url=url).status_code
        self.assertEqual(response, 422)

    def test_get_access_token(self):
        refresh_token_url = BASE_AUTH_SERVER_URL + params[cnt.GET_TOKENS_ENDPOINT]
        refresh_token = test_client.post(url=refresh_token_url, json=get_tokens()).json()[cnt.REFRESH_TOKEN][cnt.TOKEN]
        access_token_url = BASE_AUTH_SERVER_URL + params[cnt.GET_ACCESS_TOKEN_ENDPOINT]
        response = test_client.post(url=access_token_url, json=get_token(token=refresh_token)).json()

        self.assertEqual(int(response[cnt.MSG_CODE]), params[cnt.MSG_CODES][cnt.MSG_ALL_DONE])
        self.assertTrue(response['access_token'])

    def test_get_access_token_wrong(self):
        url = BASE_AUTH_SERVER_URL + params[cnt.GET_ACCESS_TOKEN_ENDPOINT]
        response = test_client.post(url=url, json=get_token()).status_code
        self.assertEqual(response, 403)
