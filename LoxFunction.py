from typing import List

import Stmt
from Environment import Environment
from LoxCallable import LoxCallable
from Return import Return


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Stmt.Function, closure: Environment, isInitializer: bool):
        self.declaration = declaration
        self.closure = closure
        self.isInitializer = isInitializer

    def call(self, interpreter: "Interpreter", arguments: List[object]):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.parameters)):
            environment.define(self.declaration.parameters[i].lexeme, arguments[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as returnValue:
            return returnValue.value

        if self.isInitializer: return self.closure.getAt(0, 'this')  # 如果函数是初始化函数，会直接返回 this
        return None

    def arity(self):
        return len(self.declaration.parameters)

    def __str__(self):
        return f"<function {self.declaration.name.lexeme} >"

    def bind(self, instance: "LoxInstance"):
        environment = Environment(self.closure)
        environment.define('this', instance)
        return LoxFunction(self.declaration, environment, self.isInitializer)
