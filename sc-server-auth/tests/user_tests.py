from tests.common import *

user_creds = {"name": "admin", "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_user_creds = {"name": "stas", "password": "a665a45923422f9d417e5867efdc4fb8a06a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_pass_creds = {"name": "admin", "password": "a665a45923422f9d417e5867efdc4fb8a06a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_token = {"token": "wrong_token"}


class TestUsers(BaseServerTestCase):
    def setUp(self) -> None:
        response = test_client.post(url=get_tokens_url, json=user_creds).json()
        self.access_token = response["access_token"]["token"]

    def test_create_user_with_wrong_token(self):
        user = create_user_request()
        response = test_client.post(url=user_url, json=user).json()
        self.assertEqual(response["detail"], "Access denied")

    def test_create_and_delete_user(self):
        user = create_user_request(token=self.access_token)
        new_user_response = test_client.post(url=user_url, json=user).json()
        exist_user_response = test_client.post(url=user_url, json=user).json()

        user_to_remove = delete_user_request(token=self.access_token)
        delete_user_response = test_client.delete(url=user_url, json=user_to_remove).json()

        self.assertEqual(int(new_user_response['msg_code']), 0)
        self.assertEqual(int(exist_user_response['msg_code']), 4)
        self.assertEqual(int(delete_user_response['msg_code']), 0)

    def test_create_user_with_wrong_password(self):
        user = create_user_request(token=self.access_token, password="ivan_006")
        response = test_client.post(url=user_url, json=user).json()
        self.assertEqual(int(response['msg_code']), 2)

    def test_create_user_with_wrong_name(self):
        user = create_user_request(token=self.access_token, name="Ivan$")
        response = test_client.post(url=user_url, json=user).json()
        self.assertEqual(int(response['msg_code']), 1)

    def test_delete_user_with_wrong_token(self):
        user_to_remove = delete_user_request()
        delete_user_response = test_client.delete(url=user_url, json=user_to_remove).json()
        self.assertEqual(delete_user_response["detail"], "Access denied")

    def test_delete_user_with_wrong_name(self):
        user_to_remove = delete_user_request(token=self.access_token, name="Unknown_user")
        delete_user_response = test_client.delete(url=user_url, json=user_to_remove).json()
        self.assertEqual(int(delete_user_response['msg_code']), 3)

    def test_get_users(self):
        response = test_client.get(url=users_url, json={"token": self.access_token}).json()
        self.assertEqual(type(response), list)

    def test_get_users_wrong_token(self):
        response = test_client.get(url=users_url, json={"token": "unknown_token"}).json()
        self.assertEqual(response["detail"], "Access denied")
