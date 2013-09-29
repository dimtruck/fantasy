import json
from wsgiref import simple_server
import inspect
import logging

class IdentityManager:

    def __init__(self):
        self.result = None
