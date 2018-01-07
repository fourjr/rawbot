class RequestError(Exception):
    '''Base class for request errors'''
    def __init__(self, resp, data):
        self.resp = resp
        self.code = resp.status
        self.error = data['message']
        super().__init__(self.error)

class Forbidden(RequestError):
    '''Raised if client does not have enough permissions to perform an action'''
    pass

class NotFound(RequestError):
    '''Raised if the provided object or ID is not found'''
    pass

class RateLimit(RequestError):
    '''Raised if the client has exceeded Discord Rate Limits'''
    def __init__(self, resp, data):
        self.local = not data['global']
        self.retry_after = data['retry_after']
        super().__init__(resp, data)
