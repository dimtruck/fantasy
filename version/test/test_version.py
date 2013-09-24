import unittest

import json
import falcon
import falcon.testing as testing
import version
import inspect
import six

class VersionResourceTest(testing.TestBase):
    def before(self):
        self.resource = version.VersionResource()
        self.api.add_route('/', self.resource)

    def after(self):
        pass

    def test_version(self):
        self.simulate_request('/')
        resp = self.resource.resp
        self.assertIn('application/json', resp._headers['Content-Type'])
        self.assertEquals(Falcon.HTTP_200,resp.status)
        keys = json.loads(resp._body)['versions']['values'][0].keys()
        self.assertIn('status', keys)
        self.assertIn('id', keys)
        self.assertIn('updated', keys)
        self.assertIn('links', keys)

class VersionDetailResourceTest(testing.TestBase):
    def before(self):
        self.detail_resource = version.VersionDetailResource()
        self.api.add_route('/{version_id}',self.detail_resource)

    def after(self):
        pass

    def test_version_detail(self):
        self.simulate_request('/v2.0')
        resp = self.detail_resource.resp
        self.assertIn('application/json',resp._headers['Content-Type'])
        self.assertEquals(Falcon.HTTP_200,resp.status)
        self.assertIn('v2.0',json.loads(resp._body)['version']['id'])
        self.assertIn('CURRENT',json.loads(resp._body)['version']['status'])
        self.assertTrue(json.loads(resp._body)['version']['updated'] != None)
        self.assertIn('self',json.loads(resp._body)['version']['links'][0]['rel'])
        self.assertIn('describedby',json.loads(resp._body)['version']['links'][1]['rel'])
        self.assertIn('describedby',json.loads(resp._body)['version']['links'][2]['rel'])
        self.assertTrue(json.loads(resp._body)['version']['media-types'] != None)

    def test_version_detail_wrong_version(self):
        self.simulate_request('/wrong_version')
        resp = self.detail_resource.resp
        self.assertIn('application/json',resp._headers['Content-Type'])
        self.assertEquals(Falcon.HTTP_300,resp.status)
        self.assertIn('status',json.loads(resp._body)['versions']['values'][0].keys())
        self.assertIn('id',json.loads(resp._body)['versions']['values'][0].keys())
        self.assertIn('updated',json.loads(resp._body)['versions']['values'][0].keys())
        self.assertIn('links',json.loads(resp._body)['versions']['values'][0].keys())

