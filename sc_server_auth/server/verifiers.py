import re


class CredentialsVerifier:
    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern)

    def __call__(self, string: str) -> bool:
        return string is not None and self.pattern.match(string)


USERNAME_PATTERN = r"^[a-zA-Z][a-zA-Z0-9-_.]{1,20}$"
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&-_]{6,}$"

username_verifier = CredentialsVerifier(USERNAME_PATTERN)
password_verifier = CredentialsVerifier(PASSWORD_PATTERN)
