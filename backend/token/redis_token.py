import datetime
import redis
import fantasy_exceptions.fantasy_exceptions as _exception
import inspect
import uuid
import yaml
import os


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


    def get_token(self, user_id):
        if user_id is None:
            raise _exception.Error("user not found.")
        ptk = self._prefix_user_id(user_id)
        token_ref = self.client.get(ptk)
        if token_ref is None:
            raise _exception.TokenNotFound(user_id)
        return token_ref

    def get_user(self, user_id):
        if user_id is None:
            raise _exception.Error("user not found.")
        ptk = self._prefix_user_id(user_id)
        token_ref = self.client.get(ptk)
        if token_ref is None:
            raise _exception.TokenNotFound(user_id)
        return token_ref


    def generate_token(self, user_id, regenerate=True):
        if user_id is None:
            raise _exception.Error("user not found.")
        if regenerate:
            token = Token(uuid.uuid1(), datetime.date.today() + datetime.timedelta(days=1))
            self._add_token(user_id, token)
        else:
            token = self.get_token(user_id)
            if token is None:
                token = Token(uuid.uuid1(), datetime.date.today() + datetime.timedelta(days=1))
                self._add_token(user_id, token)
        return token

    def _add_token(self, user_id, token):
        pass

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

    def _get_redis_client(self, client_info):
        #memcache_servers = CONF.memcache.servers.split(',')
        self._redis_client = redis.StrictRedis(host=self.client_info['host'], port=self.client_info['port'], db=self.client_info['db'])
        return self._redis_client
