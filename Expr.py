from Tokens import Token

__all__ = [
    "ExprVisitor",
    "Expr",
    "Binary",
    "Grouping",
    "Literal",
    "Unary",
]

class ExprVisitor:
    def visitBinaryExpr(self, expr: "Binary"): raise NotImplementedError

    def visitGroupingExpr(self, expr: "Grouping"): raise NotImplementedError

    def visitLiteralExpr(self, expr: "Literal"): raise NotImplementedError

    def visitUnaryExpr(self, expr: "Unary"): raise NotImplementedError


class Expr:
    def accept(self, visitor: ExprVisitor): raise NotImplementedError



class Binary(Expr):

    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):

    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLiteralExpr(self)


class Unary(Expr):

    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitUnaryExpr(self)


    