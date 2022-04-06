# SC-server-auth
Authentication server for sc-machine repository

To install poetry run command:
```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - 
```
or just do it with pip3 (not recommended):
```sh
pip3 install poetry
```

To install dependencies run command:
```sh
poetry env use 3.8
poetry shell
poetry install
```

To start auth-server run in poetry:
```
./run_server.sh
```

Current endpoints:

127.0.0.1:8000/auth/get_tokens - generate access and refresh token for current user's login and password, params: username, password, role. After check user credentials, service issues access and refresh token for future requests.
POST request-body: {"name": "admin", "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"}
127.0.0.1:8000/auth/get_access_token - generate access token, for this operation needs refresh token
POST request-body: {"token": "..."}
127.0.0.1:8000/admin/user - admin endpoint (need specific type of request for correct work), for this operation needs access token:
Examples:
POST request-body: {"name": "alex123", "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3", ""role": "patient", "lang": "ru", "access_token": "..."}
127.0.0.1:8000/admin/users - get users list, for this operation needs access token
GET request-body: {"token": "..."}
Current credentials to test: login - admin, password - a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3 (SHA256 hash)
All added endpoints respond with specific message codes:
cnt.MSG_ALL_DONE: 0,
cnt.MSG_INVALID_USERNAME: 1,
cnt.MSG_INVALID_PASSWORD: 2,
cnt.MSG_USER_NOT_FOUND: 3,
cnt.MSG_USER_IS_IN_BASE: 4

