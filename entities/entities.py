class User:
    def __init__(self, id=0,username=None,email=None,enabled=False):
        self._id = id
        self._username = username
        self._email = email
        self._enabled = enabled

    @def id():
        doc = "The id property."
        def fget(self):
            return self._id
        def fset(self, value):
            self._id = value
        def fdel(self):
            del self._id
        return locals()
    id = property(**id())

    @def username():
        doc = "The username property."
        def fget(self):
            return self._username
        def fset(self, value):
            self._username = value
        def fdel(self):
            del self._username
        return locals()
    username = property(**username())

    @def email():
        doc = "The email property."
        def fget(self):
            return self._email
        def fset(self, value):
            self._email = value
        def fdel(self):
            del self._email
        return locals()
    email = property(**email())

    @def enabled():
        doc = "The enabled property."
        def fget(self):
            return self._enabled
        def fset(self, value):
            self._enabled = value
        def fdel(self):
            del self._enabled
        return locals()
    enabled = property(**enabled())

class Token:
    def __init__(self, userid, id, expires):
        self._id = id
        self._userid = userid
        self._expires = expires

    @def id():
        doc = "The id property."
        def fget(self):
            return self._id
        def fset(self, value):
            self._id = value
        def fdel(self):
            del self._id
        return locals()
    id = property(**id())

    @def expires():
        doc = "The expires property."
        def fget(self):
            return self._expires
        def fset(self, value):
            self._expires = value
        def fdel(self):
            del self._expires
        return locals()
    expires = property(**expires())

    @def userid():
        doc = "The userid property."
        def fget(self):
            return self._userid
        def fset(self, value):
            self._userid = value
        def fdel(self):
            del self._userid
        return locals()
    userid = property(**userid())
