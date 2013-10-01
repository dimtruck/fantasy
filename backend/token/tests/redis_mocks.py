import uuid
import time

class TokenMock:
    def __init__(self):
        self._id = uuid.uuid1()
        localtime = time.localtime(time.time() + 24 * 3600)
        self._expires = localtime
        self._userid = 1234567

    @property
    def id(self):
        return self._id

    @property
    def expires(self):
        return self._expires

    @property
    def user(self):
        return self._userid

class UserMock:
    def __init__(self, token=None, userid=None, username=None, email=None, enabled=False):
        self._token = token
        self._userid = 123456
        self._username = 'username'
        self._email = 'user@email.com'
        self._enabled = True

    @property
    def id(self):
        return self._userid

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def enabled(self):
        return self._enabled

    @property
    def token(self):
        if self._token is None:
            return TokenMock()
        else:
            return self._token


class TokenInvalidMock:
    @property
    def id(self):
        return None

    @property
    def expires(self):
        return None

    @property
    def userid(self):
        return None

class RedisMock:
    def __init__(self, get_works=True, add_works=True, token=None):
        self._get = get_works
        self._add = add_works
        self._token = token

    def get(self, id):
        if self._get:
            if self._token is None:
                return UserMock()
            else:
                return UserMock(self._token)
        else:
            return None

    def mset(self, data):
        if self._add:
            return 'OK'
        else:
            return 'FAIL'

class RedisUserMock:
    def __init__(self, get_works=True, add_works=True, token=None):
        self._get = get_works
        self._add = add_works
        self._token = token

    def get(self, id):
        if self._get:
            if self._token is None:
                return TokenMock()
            else:
                return self._token
        else:
            return None

    def mset(self, data):
        if self._add:
            return 'OK'
        else:
            return 'FAIL'

class RedisInvalidMock:
    def get(self, id):
        return TokenInvalidMock()

class RedisEmptyMock:
    def get(self, id):
        return None
