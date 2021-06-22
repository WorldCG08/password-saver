class Login:
    """ Login class """

    def __init__(self, login, password, description):
        self.login = login
        self.password = password
        self.description = description

    def __str__(self):
        return f"{self.login} - {self.description}"
