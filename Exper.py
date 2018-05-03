from Tokens import Token

__all__ = [
    "ExprVisitor",
    "Expr",
    "Binary",
    "Grouping",
    "Literal",
    "Unary",
]


class Expr:
    def accept(self, visitor): raise NotImplementedError


class ExprVisitor:
    def visitBinary(self, expr: "Binary"): raise NotImplementedError

    def visitGrouping(self, expr: "Grouping"): raise NotImplementedError

    def visitLiteral(self, expr: "Literal"): raise NotImplementedError

    def visitUnary(self, expr: "Unary"): raise NotImplementedError


class Binary(Expr):

    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitBinary(self)


class Grouping(Expr):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visitGrouping(self)


class Literal(Expr):

    def __init__(self, value: "Object"):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLiteral(self)


class Unary(Expr):

    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitUnary(self)
