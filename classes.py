class User:
    def __init__(self, username: str, password: str, email: str, gender: str):
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender

    def __eq__(self, other):
        return self.username == other.username and self.password == other.password


class Login:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
