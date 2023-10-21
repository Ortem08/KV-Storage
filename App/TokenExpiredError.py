class TokenExpiredError(Exception):
    def __init__(self, message="Token has expired, please relogin"):
        self.message = message
        super().__init__(self.message)
