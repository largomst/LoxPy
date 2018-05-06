from typing import List

import Stmt
from Environment import Environment
from LoxCallable import LoxCallable


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Stmt.Function):
        self.declaration = declaration

    def call(self, interpreter: "Interpreter", arguments: List[object]):
        environment = Environment(interpreter.globals)
        for i in range(len(self.declaration.parameters)):
            environment.define(self.declaration.parameters[i].lexeme, arguments[i])

        interpreter.executeBlock(self.declaration.body, environment)

    def arity(self):
        return len(self.declaration.parameters)

    def __str__(self):
        return f"<function {self.declaration.name.lexeme} >"
