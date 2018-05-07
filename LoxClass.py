from typing import List, Dict

from LoxCallable import LoxCallable
from LoxFunction import LoxFunction
from LoxRuntimeError import LoxRuntimeError
from Tokens import Token


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods

    def __str__(self):
        return self.name

    def call(self, interpreter: "Interpreter", arguments: List[object]):
        instance = LoxInstance(self)
        return instance

    def arity(self):
        return 0

    def findMethod(self, instance: "LoxInstance", name: str):
        if name in self.methods.keys():
            return self.methods.get(name).bind(instance)
        return None


class LoxInstance:
    def __init__(self, class_: LoxClass):
        self.class_ = class_
        self.fields: Dict[str, object] = {}

    def __str__(self):
        return self.class_.name + ' instance'

    def get(self, name: Token):
        if name.lexeme in self.fields.keys():
            return self.fields.get(name.lexeme)

        method = self.class_.findMethod(self, name.lexeme)
        if method is not None:
            return method

        raise LoxRuntimeError(name, f"Undefined '{name.lexeme}'.")

    def set(self, name: Token, value: object):
        self.fields[name.lexeme] = value
