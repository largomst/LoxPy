from LoxRuntimeError import LoxRuntimeError
from Tokens import Token


class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values.keys():
            return self.values.get(name.lexeme)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}' .")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
