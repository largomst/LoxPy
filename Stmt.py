from Tokens import Token

__all__ = [
    "StmtVisitor",
    "Stmt",
    "Expression",
    "Print",
]

class StmtVisitor:
    def visitExpression(self, stmt: "Expression"): raise NotImplementedError

    def visitPrint(self, stmt: "Print"): raise NotImplementedError


class Stmt:
    def accept(self, visitor: StmtVisitor): raise NotImplementedError



class Expression(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitExpression(self)


class Print(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitPrint(self)


    