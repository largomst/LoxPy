from typing import List

from LoxCallable import LoxCallable


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

    def __str__(self):
        return self.class_.name + ' instance'
