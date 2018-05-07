from typing import List, Dict

from LoxCallable import LoxCallable
from LoxRuntimeError import LoxRuntimeError
from Tokens import Token


class LoxClass(LoxCallable):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def call(self, interpreter: "Interpreter", arguments: List[object]):
        instance = LoxInstance(self)
        return instance

    def arity(self):
        return 0


class LoxInstance:
    def __init__(self, class_: LoxClass):
        self.class_ = class_
        self.fields: Dict[str, object] = {}

    def __str__(self):
        return self.class_.name + ' instance'

    def get(self, name: Token):
        if name.lexeme in self.fields.keys():
            return self.fields.get(name.lexeme)

        raise LoxRuntimeError(name, f"Undefined '{name.lexeme}'.")

    def set(self, name: Token, value: object):
        self.fields[name.lexeme] = value

