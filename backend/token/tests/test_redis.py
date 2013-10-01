import unittest
import fantasy_exceptions.fantasy_exceptions as _exceptions
from backend.token.redis_token import RedisProvider
import inspect
import exceptions
import uuid
import redis_mocks
import entities.entities as entities
import redis
import yaml
import os
import time


class TestRedis(unittest.TestCase):
    def setUp(self):
        redis_client = redis_mocks.RedisMock()
        self.provider = RedisProvider(redis_client)

    def tearDown(self):
        pass

    # test redis connectivity
    def test_redis_connection_pass(self):
        config = yaml.load(open(os.path.join(os.getcwd(),"config","config.yaml"), 'r'))
        client_info = {'host': config['redis']['host'], 'port': config['redis']['port'], 'db': config['redis']['db']}
        self.provider = RedisProvider(config=config)
        self.assertTrue(self.provider.client.ping())


    def test_redis_connection_fail(self):
        self.provider = RedisProvider(config={'redis':{'host': 'localhost', 'port': 6379, 'db': 0}})
        self.assertRaises(redis.ConnectionError, self.provider.client.ping)

    # test token generation
    def test_token_generation_success(self):
        token = self.provider.generate_token("123456", True)
        self.assertIsNotNone(token.id)
        expiration_date = time.localtime(time.time() + 23*3600)
        self.assertTrue(token.expires > expiration_date)

    def test_token_generation_success_already_exists(self):
        redis_client = redis_mocks.RedisUserMock()
        self.provider = RedisProvider(redis_client)
        old_token = self.provider.get_token("123456")
        redis_client = redis_mocks.RedisUserMock(True, True, old_token)
        self.provider = RedisProvider(redis_client)
        token = self.provider.generate_token("123456", True)
        self.assertIsNotNone(token.id)
        self.assertNotEqual(old_token.id, token.id)
        self.assertTrue(token.expires > time.localtime(time.time() + 23*3600))

    def test_token_generation_success_already_exists_do_not_regenerate(self):
        redis_client = redis_mocks.RedisUserMock()
        self.provider = RedisProvider(redis_client)
        old_token = self.provider.get_token("123456")
        redis_client = redis_mocks.RedisMock(True, True, old_token)
        self.provider = RedisProvider(redis_client)
        token = self.provider.generate_token("123456", False)
        self.assertIsNotNone(token.id)
        self.assertEquals(token.expires, old_token.expires)
        self.assertEqual(old_token.id.hex, token.id.hex)

    def test_token_generation_fail(self):
        redis_client = redis_mocks.RedisMock(False, False)
        self.provider = RedisProvider(redis_client)
        self.assertRaises(_exceptions.UserNotFound, self.provider.generate_token, "invalid", True)

    def test_token_generation_user_none(self):
        self.assertRaises(_exceptions.Error, self.provider.generate_token, None, True)

    def test_token_generation_user_does_not_exist(self):
        redis_client = redis_mocks.RedisUserMock(False, False)
        self.provider = RedisProvider(redis_client)
        self.assertRaises(_exceptions.UserNotFound, self.provider.generate_token, "invalid", True)

    # test token retrieval
    def test_token_retrieval_valid_token(self):
        redis_client = redis_mocks.RedisUserMock()
        self.provider = RedisProvider(redis_client)
        token = self.provider.get_token("1234567890")
        self.assertIsNotNone(token.id)
        self.assertIsNotNone(token.expires)

    def test_token_retrieval_none(self):
        self.assertRaises(_exceptions.Error, self.provider.get_token, None)

    def test_token_retrieval_invalid_token(self):
        redis_client = redis_mocks.RedisMock(False, False)
        self.provider = RedisProvider(redis_client)
        self.assertRaises(_exceptions.TokenNotFound, self.provider.get_token, "111111")

    # test user retrieval
    def test_user_retrieval_valid_user(self):
        redis_client = redis_mocks.RedisMock()
        self.provider = RedisProvider(redis_client)
        user = self.provider.get_user("1234567890")
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
        self.assertTrue(user.enabled)
        self.assertIsNotNone(user.token.id)

    def test_user_retrieval_none(self):
        redis_client = redis_mocks.RedisEmptyMock()
        self.provider = RedisProvider(redis_client)
        self.assertRaises(_exceptions.Error, self.provider.get_user, None)

    def test_user_retrieval_invalid_user(self):
        redis_client = redis_mocks.RedisEmptyMock()
        self.provider = RedisProvider(redis_client)
        self.assertRaises(_exceptions.UserNotFound, self.provider.get_user, "111111")

    # add user
    def test_user_add_success(self):
        user = entities.User(username='username', email='user@email.com', enabled=True)
        self.assertEqual(self.provider.add_user(user),'OK')

    def test_user_add_user_already_exists(self):
        redis_client = redis_mocks.RedisMock(True,False)
        self.provider = RedisProvider(redis_client)
        user = entities.User(username='username', email='user@email.com', enabled=True)
        self.assertEqual(self.provider.add_user(user),'FAIL')

    def test_user_add_user_data_invalid(self):
        user = entities.User(email='user@email.com', enabled=True)
        self.assertRaises(_exceptions.UserInvalid, self.provider.add_user, user)

    # add token
    def test_token_add_success(self):
        token = entities.Token(userid='123456', id='1234567', expires=time.localtime(time.time() + 24*3600))
        self.assertEqual(self.provider.add_token(token),'OK')

    def test_token_add_token_already_exists(self):
        redis_client = redis_mocks.RedisMock(True,False)
        self.provider = RedisProvider(redis_client)
        token = entities.Token(userid='123456', id='1234567', expires=time.localtime(time.time() + 24*3600))
        self.assertEqual(self.provider.add_token(token),'FAIL')

    def test_token_add_token_data_invalid(self):
        token = entities.Token(id='1234567')
        self.assertRaises(_exceptions.TokenInvalid, self.provider.add_token, token)
        token = entities.Token(userid='1234567')
        self.assertRaises(_exceptions.TokenInvalid, self.provider.add_token, token)

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
