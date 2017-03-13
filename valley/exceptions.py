class ValidationException(Exception):

    def __init__(self, msg):
        self.error_msg = msg

    def __str__(self):
        return self.error_msg
