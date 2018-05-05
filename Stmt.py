from Expr import Expr
from Tokens import Token

__all__ = [
    "StmtVisitor",
    "Stmt",
    "Expression",
    "Print",
]

class StmtVisitor:
    def visitExpressionStmt(self, stmt: "Expression"): raise NotImplementedError

    def visitPrintStmt(self, stmt: "Print"): raise NotImplementedError


class Stmt:
    def accept(self, visitor: StmtVisitor): raise NotImplementedError



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


    