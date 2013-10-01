import datetime
import redis
import fantasy_exceptions.fantasy_exceptions as _exception
import inspect
import uuid

class Token:
    def __init__(self, id, expires):
        self._id = id
        self._expires = expires

    @property
    def id(self):
        return self._id

    @property
    def expires(self):
        return self._expires

#import redis python hook
class RedisProvider:

    def __init__(self, client=None, config=None):
        self._redis_client = client

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

    def _get_redis_client(self):
        #memcache_servers = CONF.memcache.servers.split(',')
        self._redis_client = redis.StrictRedis(host=client_info['host'], port=client_info['port'], db=client_info['db'])
        return self._redis_client
