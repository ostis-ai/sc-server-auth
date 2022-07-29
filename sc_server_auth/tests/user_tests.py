import sc_server_auth.configs.constants as cnt
from sc_server_auth.server.models import ResponseModels
from sc_server_auth.tests.common import BaseServerTestCase


class TestUsers(BaseServerTestCase):
    def setUp(self) -> None:
        response = self.test_client.post(url=self.tokens_url, json=self.get_tokens_request()).json()
        self.access_token = response[cnt.ACCESS_TOKEN][cnt.TOKEN]

    def test_delete_user(self):
        user_to_remove = self.delete_user_request(token=self.access_token)
        delete_user_response = self.test_client.delete(url=self.user_url, json=user_to_remove).json()
        self.assertEqual(int(delete_user_response[cnt.MSG_CODE]), 0)

    def test_delete_user_empty(self):
        delete_user_response = self.test_client.delete(url=self.user_url).status_code
        self.assertEqual(delete_user_response, 422)

    def test_delete_user_with_wrong_token(self):
        delete_user_response = self.test_client.delete(url=self.user_url, json=self.delete_user_request()).json()
        self.assertEqual(delete_user_response["detail"], ResponseModels.access_denied.msg_text)

    def test_delete_user_with_wrong_name(self):
        user_to_remove = self.delete_user_request(token=self.access_token, name="Unknown_user")
        delete_user_response = self.test_client.delete(url=self.user_url, json=user_to_remove).json()
        self.assertEqual(int(delete_user_response[cnt.MSG_CODE]), 3)

    def test_create_user(self):
        user = self.create_user_request(token=self.access_token)
        new_user_response = self.test_client.post(url=self.user_url, json=user).json()
        exist_user_response = self.test_client.post(url=self.user_url, json=user).json()

        self.assertEqual(int(new_user_response[cnt.MSG_CODE]), 0)
        self.assertEqual(int(exist_user_response[cnt.MSG_CODE]), 4)

    def test_create_user_empty(self):
        new_user_response = self.test_client.post(url=self.user_url).status_code
        self.assertEqual(new_user_response, 422)

    def test_create_user_with_wrong_token(self):
        response = self.test_client.post(url=self.user_url, json=self.create_user_request()).json()
        self.assertEqual(response["detail"], ResponseModels.access_denied.msg_text)

    def test_create_user_with_wrong_password(self):
        user = self.create_user_request(token=self.access_token, password="ivan_006")
        response = self.test_client.post(url=self.user_url, json=user).json()
        self.assertEqual(int(response[cnt.MSG_CODE]), 2)

    def test_create_user_with_wrong_name(self):
        user = self.create_user_request(token=self.access_token, name="Ivan$")
        response = self.test_client.post(url=self.user_url, json=user).json()
        self.assertEqual(int(response[cnt.MSG_CODE]), 1)

    def test_get_users(self):
        response = self.test_client.post(url=self.users_url, json=self.get_token_request(self.access_token)).json()
        self.assertEqual(type(response), list)

    def test_get_users_empty(self):
        response = self.test_client.post(url=self.users_url).status_code
        self.assertEqual(response, 422)

    def test_get_users_wrong_token(self):
        response = self.test_client.post(url=self.users_url, json=self.get_token_request()).json()
        self.assertEqual(response["detail"], ResponseModels.access_denied.msg_text)
