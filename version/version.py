import json
from wsgiref import simple_server
import inspect
import logging

import falcon

version_detail_json = """{
  "version": {
    "id": "v2.0",
    "status": "CURRENT",
    "updated": "2011-01-21T11:33:21-06:00",
    "links": [
      {
        "rel": "self",
        "href": "http://identity.api.rackspacecloud.com/v2.0/"
      }, {
        "rel": "describedby",
        "type": "application/pdf",
        "href": "http://docs.rackspacecloud.com/auth/api/v2.0/auth-client-devguide-latest.pdf"
      }, {
        "rel": "describedby",
        "type": "application/vnd.sun.wadl+xml",
        "href": "http://docs.rackspacecloud.com/auth/api/v2.0/auth.wadl"
      }
    ],
    "media-types": [
      {
        "base": "application/xml",
        "type": "application/vnd.openstack.identity+xml;version=2.0"
      }, {
        "base": "application/json",
        "type": "application/vnd.openstack.identity+json;version=2.0"
      }
    ]
  }
}"""

version_json = """{
  "versions": {
    "values": [
      {
        "id": "v1.0",
        "status": "DEPRECATED",
        "updated": "2009-10-09T11:30:00Z",
        "links": [
          {
            "rel": "self",
            "href": "http://example.com/v1.0/"
          }
        ]
      }, {
        "id": "v1.1",
        "status": "CURRENT",
        "updated": "2010-12-12T18:30:02.25Z",
        "links": [
          {
            "rel": "self",
            "href": "http://example.com/v1.1/"
          }
        ]
      }, {
        "id": "v2.0",
        "status": "BETA",
        "updated": "2011-05-27T20:22:02.25Z",
        "links": [
          {
            "rel": "self",
            "href": "http://example.com/v2.0/"
          }
        ]
      }
    ]
  }
}"""

class VersionResource:

	def __init__(self):
		self.result = None

	def on_get(self, request, resp):
		resp.status = falcon.HTTP_200
		self.req, self.resp = request, resp
		resp.body = version_json

class VersionDetailResource:
	def __init__(self):
		self.result = None

	def on_get(self, request, resp, version_id):
		self.req, self.resp = request, resp
		if version_json != None and version_id != None and version_id == 'v2.0':
			resp.status = falcon.HTTP_200
			resp.body = version_detail_json
		else:
			resp.status = falcon.HTTP_300
			resp.body = version_json


version = VersionResource()
version_detail = VersionDetailResource()

wsgi_app = api = falcon.API()

api.add_route('/{version_id}',version_detail)
api.add_route('/',version)

app = application = api

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
  httpd = simple_server.make_server('127.0.0.1', 1235, app)
  httpd.serve_forever()

