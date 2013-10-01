import exceptions

class Error(StandardError):
    code = None
    title = None
    message_format = None

    def __init__(self, message=None, **kwargs):
        message = self._build_message(message, **kwargs)
        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        if not message:
            message = self.message_format % kwargs
        return message


class NotFound(Error):
    message_format = "Could not find, %(target)s."
    code = 404
    title = 'Not Found'

class UserNotFound(NotFound):
    message_format = "Could not find user, %(user_id)s."

class UserInvalid(NotFound):
    message_format = "Specified invalid user."

class TokenNotFound(NotFound):
    message_format = "Could not find token for user, %(user_id)s."
