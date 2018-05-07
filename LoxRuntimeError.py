import ErrorState
from Tokens import Token


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token

        self.message = message


def runtimeError(error: LoxRuntimeError):
    print(f"[line {error.token.line}] {error.message}")
    ErrorState.hadRuntimeError = True
