import uuid
import datetime

class TokenMock:
    @property
    def id(self):
        return uuid.uuid1()

    @property
    def expires(self):
        return datetime.date.today() + datetime.timedelta(days=1)

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

    def add(self, data):
        if self._add:
            return 1
        else:
            return 0

class RedisInvalidMock:
    def get(self, id):
        return TokenInvalidMock()

class RedisEmptyMock:
    def get(self, id):
        return None
