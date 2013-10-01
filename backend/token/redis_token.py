import time
import redis
import fantasy_exceptions.fantasy_exceptions as _exception
import inspect
import uuid
import yaml
import os
import entities.entities as _entities


'''
redis provider will allow user to:
    get users
    get tokens from users
    add users
    add tokens to users
    remove users
    remove tokens from users
'''
class RedisProvider:

    def __init__(self, client=None, config=None):
        self._redis_client = client
        if config is None:
            config = yaml.load(open(os.path.join(os.getcwd(),"config","config.yaml"), 'r'))
        self.client_info = {'host': config['redis']['host'], 'port': config['redis']['port'], 'db': config['redis']['db']}


    '''
    1. check if token is specified
    2. get token prefix
    3. search for token

    '''
    def get_token(self, token_id):
        if token_id is None:
            raise _exception.Error("user not found.")
        ptk = self._prefix_token_id(token_id)
        token_ref = self.client.get(ptk)
        if token_ref is None:
            raise _exception.TokenNotFound(token_id)
        return token_ref

    def get_user(self, user_id):
        if user_id is None:
            raise _exception.Error("user not found.")
        ptk = self._prefix_user_id(user_id)
        user_ref = self.client.get(ptk)
        if user_ref is None:
            raise _exception.UserNotFound(user_id)
        return user_ref

    '''
    1. check if user_id is specified
    2. check if user exists

    '''
    def generate_token(self, user_id, regenerate=True):
        if user_id is None:
            raise _exception.Error("user not found.")
        user = self.get_user(user_id)
        if user is None:
            raise _exception.Error("user not found.")
        else:
            if regenerate:
                token = _entities.Token(uuid.uuid1(), time.localtime(time.time() + 24*3600), user_id)
                self.add_token(token)
            else:
                token = user.token
        return token

    def add_token(self, token=None):
        if token is None or token.expires is None or token.id is None:
            raise _exception.TokenInvalid
        return self.client.mset(token)

    def add_user(self, user):
        if user is None or user.username is None:
            raise _exception.UserInvalid
        return self.client.mset(user.__dict__)

    def _prefix_token_id(self, token_id):
        return 'tokens-%s' % token_id.encode('utf-8')

    def _prefix_user_id(self, user_id):
        return 'usertokens-%s' % user_id.encode('utf-8')

    @property
    def client(self):
        return self._redis_client or self._get_redis_client()

    @property
    def client_info(self):
        return self._client_info

    @client_info.setter
    def client_info(self, value):
        self._client_info = value

    def _get_redis_client(self):
        #memcache_servers = CONF.memcache.servers.split(',')
        self._redis_client = redis.StrictRedis(host=self.client_info['host'], port=self.client_info['port'], db=self.client_info['db'])
        return self._redis_client
