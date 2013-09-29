import unittest

import json
import falcon
import falcon.testing as testing
import identity
import manager
import inspect
import six

class IdentityTokenListResourceTest(testing.TestBase):
    def before(self):
        self.manager = manager.IdentityManager()
        self.resource = identity.IdentityTokenListResource()
        #post /version/tokens with user id and api key
        self.api.add_route('/{version_id}/tokens', self.resource)
        #get /version/tokens/tokenid
        #self.api.add_route('/{version_id}/tokens/{token}', self.resource)

    def after(self):
        pass

    def test_valid_token_generation(self):
        headers = {'Content-Type': 'application/json'}
        body = """{
    "auth": {
        "username": "demoauthor",
        "apiKey": "aaaaa-bbbbb-ccccc-12345678"
    }
}"""
        self.simulate_request('/v1.0/tokens', method = 'POST', headers = headers, body = body)
        resp = self.resource.resp
        self.assertIn('application/json', resp._headers['Content-Type'])
        self.assertEquals(falcon.HTTP_200,resp.status)
        access = json.loads(resp._body)["access"]
        self.assertEquals(4, len(access['serviceCatalog']))
        self.assertIn('id', access['user'])
        self.assertEquals('aaaaa-bbbbb-ccccc-dddd', access['token']['id'])
        self.assertTrue(access['token']['expires'] != None)
        self.assertEquals(1, len(access['user']['roles']))

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
        self.assertEquals(falcon.HTTP_401,resp.status)

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
        self.assertEquals(falcon.HTTP_401,resp.status)

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
        self.assertEquals(falcon.HTTP_403,resp.status)
