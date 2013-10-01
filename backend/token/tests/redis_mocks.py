import uuid
import datetime

class TokenMock:
    @property
    def id(self):
        return uuid.uuid1()

    @property
    def expires(self):
        return datetime.datetime.now() + datetime.timedelta(days=1)

class UserMock:
    @property
    def id(self):
        return 123456

    @property
    def username(self):
        return 'username'

    @property
    def email(self):
        return 'user@email.com'

    @property
    def enabled(self):
        return True

    @property
    def token(self):
        return TokenMock()


class TokenInvalidMock:
    @property
    def id(self):
        return None

    @property
    def expires(self):
        return None

class RedisMock:
    def __init__(self, get_works=True, add_works=True):
        self._get = get_works
        self._add = add_works

    def get(self, id):
        if self._get:
            return TokenMock()
        else:
            return None

    def mset(self, data):
        if self._add:
            return 'OK'
        else:
            return 'FAIL'

class RedisUserMock:
    def __init__(self, get_works=True, add_works=True):
        self._get = get_works
        self._add = add_works

    def get(self, id):
        if self._get:
            return UserMock()
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
