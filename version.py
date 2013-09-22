import json
from wsgiref import simple_server
import inspect
import logging

import falcon

class VersionResource:

	def __init__(self):
		self.result = None

	def on_get(self, request, resp):
		print "ENVIRONMENT: %s " % request.env
		print "HEADERS: %s " % request._headers
		print "METHOD: %s " % request.method
		print "PARAMETERS: %s " % request._params
		print "PATH: %s " % request.path
		print "QUERY STRING: %s " % request.query_string
		print "STREAM: %s " % request.stream
		print "ERRORS: %s " % request._wsgierrors
		resp.status = falcon.HTTP_200
		resp.body = """{
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

class VersionDetailResource:

	def on_get(self, req, resp, version_id):
		
		print inspect.getmembers(self)
		print "version: %s " % version_id
		print "ENVIRONMENT: %s " % req.env
		print "HEADERS: %s " % req._headers
		print "METHOD: %s " % req.method
		print "PARAMETERS: %s " % req._params
		print "PATH: %s " % req.path
		print "QUERY STRING: %s " % req.query_string
		print "STREAM: %s " % req.stream
		print "ERRORS: %s " % req._wsgierrors
		resp.status = falcon.HTTP_200
		print resp.__slots__


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

