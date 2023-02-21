from paux.exception._base import AbstractEXP


class ExecuteException(AbstractEXP):
    def __init__(self, msg):
        self.error_msg = msg

