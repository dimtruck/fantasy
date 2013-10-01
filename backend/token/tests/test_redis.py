import unittest
import datetime
import fantasy_exceptions.fantasy_exceptions as _exceptions
from backend.token.redis_token import RedisProvider
import inspect
import exceptions
import uuid

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

class TestRedis(unittest.TestCase):
    def setUp(self):
        redis_client = RedisMock()
        self.provider = RedisProvider(redis_client)

    def tearDown(self):
        pass

    # test redis connectivity
    def test_redis_connection_pass(self):
        self.provider = RedisProvider({'host': '50.56.175.34', 'port': 6379, 'db': 0})
        print inspect.getmembers(self.provider.client)

    def test_redis_connection_fail(self):
        self.provider = RedisProvider({'host': '50.56.175.34', 'port': 6379, 'db': 0})
        print inspect.getmembers(self.provider.client)

    # test token generation
    def test_token_generation_success(self):
        token = self.provider.generate_token("123456", True)
        self.assertIsNotNone(token.id)
        self.assertTrue(token.expires > datetime.date.today() + datetime.timedelta(days=1))

    def test_token_generation_success_already_exists(self):
        old_token = self.provider.get_token("123456")
        token = self.provider.generate_token("123456", True)
        self.assertIsNotNone(token.id)
        self.assertTrue(token.expires > datetime.date.today() + datetime.timedelta(days=1))
        self.assertNotEqual(old_token.id, token.id)

    def test_token_generation_success_already_exists_do_not_regenerate(self):
        old_token = self.provider.get_token("123456")
        token = self.provider.generate_token("123456", False)
        self.assertIsNotNone(token.id)
        self.assertTrue(token.expires > datetime.date.today() + datetime.timedelta(days=1))
        self.assertEqual(old_token.id, token.id)

    def test_token_generation_fail(self):
        token = self.provider.generate_token("invalid", True)
        self.assertIsNone(token)
        self.assertRaises(exceptions.UserNotFound)

    def test_token_generation_user_none(self):
        self.assertRaises(_exceptions.Error, self.provider.generate_token, None, True)

    def test_token_generation_user_does_not_exist(self):
        self.assertRaises(_exceptions.UserNotFound, self.provider.generate_token, "invalid", True)

    # test token retrieval
    def test_token_retrieval_valid_token(self):
        token = self.provider.get_token("1234567890")
        self.assertIsNotNone(token.id)
        self.assertIsNotNone(token.expires)

    def test_token_retrieval_none(self):
        self.assertRaises(_exceptions.Error, self.provider.get_token, None)

    def test_token_retrieval_invalid_token(self):
        self.assertRaises(_exceptions.TokenNotFound, self.provider.get_token, "111111")

    # test user retrieval
    def test_user_retrieval_valid_user(self):
        token = self.provider.get_user("1234567890")
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
        self.assertTrue(user.enabled)

    def test_user_retrieval_none(self):
        redis_client = RedisEmptyMock()
        self.provider = RedisProvider(redis_client)
        self.assertRaises(_exceptions.Error, self.provider.get_user, None)

    def test_user_retrieval_invalid_user(self):
        redis_client = RedisEmptyMock()
        self.provider = RedisProvider(redis_client)
        self.assertRaises(_exceptions.UserNotFound, self.provider.get_user, "111111")

    # add user
    def test_user_add_success(self):
        user = User('username','user@email.com', True)
        self.assertTrue(self.provider.add_user(user) > 0)

    def test_user_add_user_already_exists(self):
        redis_client = RedisMock(True,False)
        self.provider = RedisProvider(redis_client)
        user = User('username','user@email.com', True)
        self.assertTrue(self.provider.add_user(user) == 0)

    def test_user_add_user_data_invalid(self):
        user = User('','user@email.com', True)
        self.assertRaises(_exceptions.UserInvalid, self.provider.add_user, user)

    # add token
    def test_token_add_success(self):
        token = Token('1234567890')
        self.assertTrue(self.provider.add_token(token) > 0)

    def test_token_add_user_already_exists(self):
        redis_client = RedisMock(True,False)
        self.provider = RedisProvider(redis_client)
        token = Token('1234567890')
        self.assertTrue(self.provider.add_token(token) == 0)

    def test_token_add_user_data_invalid(self):
        token = Token(None)
        self.assertRaises(_exceptions.UserInvalid, self.provider.add_token, token)

    # remove user
    def test_remove_user_success(self):
        pass

    def test_remove_user_not_found(self):
        pass

    def test_remove_user_none(self):
        pass

    # remove token
    def test_remove_token_success(self):
        pass

    def test_remove_token_not_found(self):
        pass

    def test_remove_token_none(self):
        pass
