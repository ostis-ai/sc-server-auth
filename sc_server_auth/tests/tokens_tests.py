import sc_server_auth.configs.constants as cnt
from sc_server_auth.server.models import ResponseModels
from sc_server_auth.tests.common import BaseServerTestCase


class ServerTest(BaseServerTestCase):
    def test_get_tokens(self):
        response = self.test_client.post(url=self.tokens_url, json=self.get_tokens_request()).json()

        self.assertEqual(response[cnt.MSG_CODE], ResponseModels.all_done.msg_code)
        self.assertTrue(response[cnt.ACCESS_TOKEN])
        self.assertTrue(response[cnt.REFRESH_TOKEN])

    def test_get_tokens_no_user_in_db(self):
        response = self.test_client.post(url=self.tokens_url, json=self.get_tokens_request(name="Stas")).json()
        self.assertEqual(response[cnt.MSG_CODE], ResponseModels.user_not_found.msg_code)

    def test_get_tokens_empty(self):
        response = self.test_client.post(url=self.tokens_url).status_code
        self.assertEqual(response, 422)

    def test_get_access_token(self):
        refresh_token = self.test_client.post(url=self.tokens_url, json=self.get_tokens_request()).json()[
            cnt.REFRESH_TOKEN
        ][cnt.TOKEN]

        response = self.test_client.post(
            url=self.access_token_url, json=self.get_token_request(token=refresh_token)
        ).json()

        self.assertEqual(response[cnt.MSG_CODE], ResponseModels.all_done.msg_code)
        self.assertTrue(response[cnt.ACCESS_TOKEN])

    def test_get_access_token_wrong(self):
        response = self.test_client.post(url=self.access_token_url, json=self.get_token_request()).status_code
        self.assertEqual(response, 403)

    def test_get_access_token_empty(self):
        response = self.test_client.post(url=self.access_token_url).status_code
        self.assertEqual(response, 422)
