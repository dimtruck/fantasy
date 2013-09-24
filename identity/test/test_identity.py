import unittest

import json
import falcon
import falcon.testing as testing
import version
import inspect
import six

class IdentityTokensResourceTest(testing.TestBase):
    def before(self):
        identity = identity.IdentityManager()
        self.resource = identity.IdentityTokensResource()
        #post /version/tokens with user id and api key
        self.api.add_route('/{version_id}/tokens', self.resource)
        #get /version/tokens/tokenid
        self.api.add_route('/{version_id}/tokens/{token}', self.resource)

    def after(self):
        pass

    def test_valid_token_generation(self):
        body = """{
    "auth": {
        "username": "demoauthor",
        "apiKey": "aaaaa-bbbbb-ccccc-12345678"
    }
}"""
        self.simulate_request('/v1.0/tokens', method = 'POST', headers = headers, body = body)
        resp = self.resource.resp
        self.assertIn('application/json', resp._headers['Content-Type'])
        self.assertEquals(Falcon.HTTP_200,resp.status)
        access = json.loads(resp._body)['access']
        keys = access['serviceCatalog'].keys()
        self.assertEquals(4, len(keys))
        self.assertIn('id', access['id'])
        self.assertEquals('updated', access['token']['id'])
        self.assertTrue(access['token']['expires'] != None)
        self.assertIn(3, len(access['roles']keys()))

    def test_token_generation_invalid_api(self):
        headers = {'Content-Type': 'application/json'}
        body = """{
    "auth": {
        "username": "demoauthor",
        "apiKey": "not-valid-api"
    }
}"""
        self.simulate_request('/v1.0/tokens', method = 'POST', headers = headers, body = body)
        resp = self.resource.resp
        self.assertIn('application/json', resp._headers['Content-Type'])
        self.assertEquals(Falcon.HTTP_401,resp.status)

    def test_token_generation_invalid_user(self):
        headers = {'Content-Type': 'application/json'}
        body = """{
    "auth": {
        "username": "invalid",
        "apiKey": "aaaaa-bbbbb-ccccc-12345678"
    }
}"""
        self.simulate_request('/v1.0/tokens', method = 'POST', headers = headers, body = body)
        resp = self.resource.resp
        self.assertIn('application/json', resp._headers['Content-Type'])
        self.assertEquals(Falcon.HTTP_401,resp.status)

    def test_token_generation_disabled_user(self):
        headers = {'Content-Type': 'application/json'}
        body = """{
    "auth": {
        "username": "disabled",
        "apiKey": "aaaaa-bbbbb-ccccc-12345678"
    }
}"""
        self.simulate_request('/v1.0/tokens', method = 'POST', headers = headers, body = body)
        resp = self.resource.resp
        self.assertIn('application/json', resp._headers['Content-Type'])
        self.assertEquals(Falcon.HTTP_403,resp.status)

class IdentityUsersResourceTest(testing.TestBase):
    def before(self):
        identity = identity.IdentityManager()
        self.resource = identity.IdentityUsersResource()
        #get /version/users -X-Auth-Token: token
        #get /version/users?name=NAME -X-Auth-Token: token
        #get /version/users/ID -X-Auth-Token: token
        #get /version/users?email=EMAIL -X-Auth-Token: token
        #post /version/users -X-Auth-Token: token

    def test_valid_users(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/users', headers = headers)
        resp = """{
    "users":[{
            "id":"123456",
            "username":"jqsmith",
            "email":"john.smith@example.org",
            "enabled":true
        },
        {
            "id":"1234562",
            "username":"jqsmith2",
            "email":"john.smith2@example.org",
            "enabled":true
        }
    ],
    "users_links":[]
}"""

    def test_valid_user_by_name(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/users?name=jqsmith', headers = headers)
        resp = """{
    "user":{
            "id":"123456",
            "username":"jqsmith",
            "email":"john.smith@example.org",
            "enabled":true
        }
}"""

    def test_valid_user_by_id(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/users/123456', headers = headers)
        resp = """{
    "user":{
            "id":"123456",
            "username":"jqsmith",
            "email":"john.smith@example.org",
            "enabled":true
        }
}"""

    def test_valid_user_by_email(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/users?email=john.smith@example.org', headers = headers)
        resp = """{
    "user":{
            "id":"123456",
            "username":"jqsmith",
            "email":"john.smith@example.org",
            "enabled":true
        }
}"""

    def test_create_valid_user(self):
        headers = {'Content-Type': 'application/json'}
        body = """{
    "user": {
        "username": "jqsmith",
        "email": "john.smith@example.org",
        "enabled" true
    }
}"""
        self.simulate_request('/v1.0/users', method = 'POST', headers = headers, body = body)
        resp = """{
    "user":{
            "id":"123456",
            "username":"jqsmith",
            "email":"john.smith@example.org",
            "enabled":true
        }
}"""
