class User:
    def __init__(self, userid=0, username=None, email=None, enabled=False):
        self._id = userid
        self._username = username
        self._email = email
        self._enabled = enabled

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

class Token:
    def __init__(self, id=None, expires=None):
        self._id = id
        self._expires = expires

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def expires(self):
        return self._expires

    @expires.setter
    def expires(self, value):
        self._expires = value


