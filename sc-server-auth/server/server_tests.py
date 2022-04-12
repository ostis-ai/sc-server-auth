import unittest
import requests
from config import params
from server import constants as cnt

user_creds = {"name": "admin", "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_user_creds = {"name": "stas", "password": "a665a45923422f9d417e5867efdc4fb8a06a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_pass_creds = {"name": "admin", "password": "a665a45923422f9d417e5867efdc4fb8a06a1f3fff1fa07e998e86f7f7a27ae3"}
wrong_token = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJzYy1hdXRoLXNlcnZlciIsImV4cCI6MTY0OTQxNTQzNC42MDYyNzQ4LCJ1c2VybmFtZSI6ImFkbWluIn0.a2a3nzcOeKaJ0cccN4NBP-FoisagL93MA9f43CpWWlUUaucoXugtxDtLT2MSd0kYH4G0OwRggYHwQkI5X09-jCt5q3iD737NVX0_-MGA135WtsgJL9NLPjSNHfvXcsx5h7G4gq2XZlAkvBHWcTD55aEd7JZnAlSwqemUNS3uayIHQQVs1GvL-C65As3BXVlzCuUuOfFcCH9fGCdIaaM7SyS0It8sn0wpt-z-xXuLHpwDomagWJZOa0aHxgwlqfse07eP1UHZR0qSKDNFGKGKrb_ohKkEH7KhONdOw5HyllwLI1Ivofp6e6OsBgE25ekODnK8pjnA8sESBGjOxhTHsQ"}

class ServerTest(unittest.TestCase):
    def test_get_tokens(self):
        response = requests.post(url=f'{params[cnt.HOST]}:{params[cnt.PORT]}{params[cnt.GET_TOKENS_ENDPOINT]}', json=user_creds).json()
        self.assertEqual(response['msg_code'], 0)
        self.assertTrue(response['access_token'])
        self.assertTrue(response['refresh_token'])

    def test_get_tokens_no_user_in_db(self):
        response = requests.post(url=f'{params[cnt.HOST]}:{params[cnt.PORT]}{params[cnt.GET_TOKENS_ENDPOINT]}', json=wrong_user_creds).json()
        self.assertEqual(response['msg_code'], params[cnt.MSG_CODES][cnt.MSG_USER_NOT_FOUND])

    def test_get_tokens_empty(self):
        response = requests.post(url=f'{params[cnt.HOST]}:{params[cnt.PORT]}{params[cnt.GET_TOKENS_ENDPOINT]}').status_code
        self.assertEqual(response, 422)

    def test_get_access_token(self):
        refresh_token = requests.post(url=f'{params[cnt.HOST]}:{params[cnt.PORT]}{params[cnt.GET_TOKENS_ENDPOINT]}', json=user_creds).json()['refresh_token']['token']
        response = requests.post(url=f'{params[cnt.HOST]}:{params[cnt.PORT]}{params[cnt.GET_ACCESS_TOKEN_ENDPOINT]}', json={'token': refresh_token}).json()
        self.assertEqual(response['msg_code'], '0')
        self.assertTrue(response['access_token'])

    def test_get_access_token_wrong(self):
        response = requests.post(url=f'{params[cnt.HOST]}:{params[cnt.PORT]}{params[cnt.GET_ACCESS_TOKEN_ENDPOINT]}', json=wrong_token).status_code
        self.assertEqual(response, 403)

    def test_get_access_token_empty(self):
        response = requests.post(url=f'{params[cnt.HOST]}:{params[cnt.PORT]}{params[cnt.GET_TOKENS_ENDPOINT]}').status_code
        self.assertEqual(response, 422)


if __name__ == '__main__':
    unittest.main()
