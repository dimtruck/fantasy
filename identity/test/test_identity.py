import unittest

import json
import falcon
import falcon.testing as testing
import identity
import manager
import inspect
import six

class IdentityUsersResourceTest(testing.TestBase):
    def before(self):
        self.manager = manager.IdentityManager()
        self.resource = identity.IdentityUsersResource()
        #get /version/users -X-Auth-Token: user-token
        #get /version/users?name=NAME -X-Auth-Token: user-token
        #get /version/users/ID -X-Auth-Token: user-token
        #get /version/users?email=EMAIL -X-Auth-Token: user-token
        #post /version/users -X-Auth-Token: user-token
        #post /version/users/ID -X-Auth-Token: user-token
        #delete /version/users/ID -X-Auth-Token: user-token

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
        headers = {
          'Content-Type': 'application/json',
          'X-Auth-Token' : 'my-token'
        }
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

    def test_update_valid_user(self):
        headers = {
          'Content-Type': 'application/json',
          'X-Auth-Token' : 'my-token'
        }
        body = """{
    "user": {
        "id":"123456",
        "username": "jqsmith",
        "email": "john.smith@example.org",
        "enabled": true
    }
}"""
        self.simulate_request('/v1.0/users/123456', method = 'POST', headers = headers, body = body)
        resp = """{
    "user":{
            "id":"123456",
            "username":"jqsmith",
            "email":"john.smith@example.org",
            "enabled":true
        }
}"""

    def test_delete_valid_user(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/users/123456', method = 'DELETE', headers = headers)
        resp = """{
    "user":{
            "id":"123456",
            "username":"jqsmith",
            "email":"john.smith@example.org",
            "enabled":true
        }
}"""

class IdentityRolesResourceTest(testing.TestBase):
    def before(self):
        self.manager = manager.IdentityManager()
        self.resource = identity.IdentityRolesResource()
        #get /version/roles -X-Auth-Token: admin-token
        #get /version/roles/ROLEID -X-Auth-Token: user-token
        #PUT /version/users/ID/roles/ROLEID -X-Auth-Token: user-token
        #DELETE /version/users/ID/roles/ROLEID -X-Auth-Token: user-token
        #GET /version/users/ID/roles -X-Auth-Token: user-token

    def test_list_roles(self):
        headers = {'X-Auth-Token' : 'admin-token'}
        self.simulate_request('/v1.0/roles', headers = headers)
        resp = """{
    "roles":[{
            "id":"123",
            "name":"football:admin",
            "description":"football admin"
        },
        {
            "id":"124",
            "name":"football:create",
            "description":"football creator"
        }
    ]
}"""

    def test_valid_role_by_id(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/roles/123', headers = headers)
        resp = """{
    "role":{
            "id":"123",
            "name":"football:admin",
            "description":"football admin"
        }
}"""

    def test_add_valid_role_to_valid_user(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/users/123456/roles/123', headers = headers, method = 'PUT')

    def test_delete_valid_role_from_valid_user(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/users/123456/roles/123', headers = headers, method = 'DELETE')

    def test_list_valid_user_roles(self):
        headers = {'X-Auth-Token' : 'my-token'}
        self.simulate_request('/v1.0/users/123456/roles', headers = headers)
        resp = """{
    "roles":[{
            "id":"123",
            "name":"football:admin",
            "description":"football admin"
        },
        {
            "id":"124",
            "name":"football:create",
            "description":"football creator"
        }
    ],
    "roles_links":[]
}"""
