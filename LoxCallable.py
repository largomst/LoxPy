from typing import List

from Interpreter import Interpreter


class LoxCallable:
    def arity(self)->int:
        pass

    def call(self, interpreter: Interpreter, arguments: List[object])->object:
        pass

