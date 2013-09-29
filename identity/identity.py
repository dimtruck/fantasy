import json
from wsgiref import simple_server
import inspect
import logging

import falcon

example_token_json = json.loads("""{
  "access": {
    "serviceCatalog": [
        {
            "endpoints": [
               {
                    "publicURL": "https://football.example.com/v2/12345"
                }
            ],
            "name": "football",
            "type": "sport"
        },
        {
            "endpoints": [
               {
                    "publicURL": "https://soccer.example.com/v2/12345"
                }
            ],
            "name": "soccer",
            "type": "sport"
        },
        {
            "endpoints": [
               {
                    "publicURL": "https://baseball.example.com/v2/12345"
                }
            ],
            "name": "baseball",
            "type": "sport"
        },
        {
            "endpoints": [
               {
                    "publicURL": "https://lacrosse.example.com/v2/12345"
                }
            ],
            "name": "lacrosse",
            "type": "sport"
        }
    ],
    "token": {
        "expires": "2012-04-13T13:15:00.000Z",
        "id": "aaaaa-bbbbb-ccccc-dddd"
    },
    "user": {
        "id": "161418",
        "name": "demoauthor",
        "roles": [
            {
                "description": "User Admin Role.",
                "id": "3",
                "name": "identity:user-admin"
            }
        ]
    }
  }
}""")

class IdentityTokenListResource:

    def __init__(self):
        self.result = None

    def on_post(self, request, resp, version_id):
        #check req body for user and password
        #auth against identity manager
        #respond with new token
        self.req, self.resp = request, resp
        if request != None:
            try:
                raw_json = request.stream.read()
            except Exception:
                raise falcon.HTTPError(falcon.HTTP_400,
                                   'Read Error',
                                   'Could not read the request body.')
            try:
                creds = json.loads(raw_json, 'utf-8')
                print creds
                if creds['auth']['username'] == 'demoauthor' and creds['auth']['apiKey'] == 'aaaaa-bbbbb-ccccc-12345678':
                    resp.body = json.dumps(example_token_json)
                    resp.status = falcon.HTTP_200
                elif creds['auth']['username'] == 'disabled':
                     resp.status = falcon.HTTP_403
                else:
                    resp.status = falcon.HTTP_401
            except Exception:
                resp.status = falcon.HTTP_400
                raise falcon.HTTPError(falcon.HTTP_400,
                                   'Read Error',
                                   'Could not read the request body.')

        else:
            resp.status = falcon.HTTP_400

class IdentityUsersResource:

    def __init__(self):
        self.result = None

    def on_get(self, request, resp):
        resp.status = falcon.HTTP_200
        self.req, self.resp = request, resp
        resp.body = version_json

class IdentityRolesResource:

    def __init__(self):
        self.result = None

    def on_get(self, request, resp):
        resp.status = falcon.HTTP_200
        self.req, self.resp = request, resp
        resp.body = version_json

identity_tokens = IdentityTokenListResource()
identity_users = IdentityUsersResource()
identity_roles = IdentityRolesResource()

wsgi_app = api = falcon.API()

#post /version/tokens with user id and api key
#get /version/tokens/tokenid
api.add_route('/{version_id}/tokens',identity_tokens)
#api.add_route('/{version_id}/tokens/{token_id}',identity_tokens)

#get /version/users -X-Auth-Token: user-token
#get /version/users?name=NAME -X-Auth-Token: user-token
#get /version/users/ID -X-Auth-Token: user-token
#get /version/users?email=EMAIL -X-Auth-Token: user-token
#post /version/users -X-Auth-Token: user-token
#post /version/users/ID -X-Auth-Token: user-token
#delete /version/users/ID -X-Auth-Token: user-token
api.add_route('/{version_id}/users',identity_users)
api.add_route('/{version_id}/users?name={name}',identity_users)
api.add_route('/{version_id}/users/{user_id}',identity_users)
api.add_route('/{version_id}/users?email={email}',identity_users)


#get /version/roles -X-Auth-Token: admin-token
#get /version/roles/ROLEID -X-Auth-Token: user-token
#PUT /version/users/ID/roles/ROLEID -X-Auth-Token: user-token
#DELETE /version/users/ID/roles/ROLEID -X-Auth-Token: user-token
#GET /version/users/ID/roles -X-Auth-Token: user-token
api.add_route('/{version_id}/roles',identity_roles)
api.add_route('/{version_id}/roles/{role_id}',identity_roles)
api.add_route('/{version_id}/users/{user_id}/roles/{role_id}',identity_roles)
api.add_route('/{version_id}/users/{user_id}/roles',identity_roles)

app = application = api

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
  httpd = simple_server.make_server('127.0.0.1', 1235, app)
  httpd.serve_forever()

