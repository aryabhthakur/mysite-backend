class InfoNotFoundError(Exception):
    def __init__(self):
        self.status_code = 404
        self.detail = "Info Not Found"

class AlreadyExistError(Exception):
    def __init__(self):
        self.status_code = 200
        self.detail = "Info already exists"

class NotAuthorizedError(Exception):
    def __init__(self):
        self.status_code = 401
        self.detail = "Not Authorized"