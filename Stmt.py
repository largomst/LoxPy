from typing import List

from Expr import Expr
from Tokens import Token

__all__ = [
    "StmtVisitor",
    "Stmt",
    "Block",
    "Expression",
    "Print",
    "Var",
]

class StmtVisitor:
    def visitBlockStmt(self, stmt: "Block"): raise NotImplementedError

    def visitExpressionStmt(self, stmt: "Expression"): raise NotImplementedError

    def visitPrintStmt(self, stmt: "Print"): raise NotImplementedError

    def visitVarStmt(self, stmt: "Var"): raise NotImplementedError


class Stmt:
    def accept(self, visitor: StmtVisitor): raise NotImplementedError



class Block(Stmt):

    def __init__(self, statements: List[Stmt]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor):
        return visitor.visitBlockStmt(self)


class Expression(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitPrintStmt(self)


class Var(Stmt):

    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor):
        return visitor.visitVarStmt(self)


    