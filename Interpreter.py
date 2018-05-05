from typing import List

import Expr
import Stmt
from Tokens import TokenType, Token
from LoxRuntimeError import LoxRuntimeError, runtimeError


class Interpreter(Expr.ExprVisitor, Stmt.StmtVisitor):
    def visitLiteralExpr(self, expr: Expr.Literal) -> object:
        return expr.value

    def visitUnaryExpr(self, expr: Expr.Unary):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.checkNumberOperand(expr.operator, right)
            return -float(right)
        elif expr.operator == TokenType.BANG:
            return not self.isTruthy(right)

        # Unreachable
        return None

    # REVIEW: 这里用默认参数来替代实现 Java 的 Overloading，看起来不太漂亮
    def checkNumberOperand(self, operator: Token, left: object, right: object = None):
        if right is None:
            if isinstance(left, float): return
            raise LoxRuntimeError(operator, "Operand must be number")
        else:
            if isinstance(left, float) and isinstance(right, float): return
            raise LoxRuntimeError(operator, "Operator must be number.")

    def visitGroupingExpr(self, expr: Expr.Grouping) -> object:
        return self.evaluate(expr.expression)

    def visitBinaryExpr(self, expr: Expr.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        optype = expr.operator.type
        if optype == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        elif optype == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)
        elif optype == TokenType.GREATER:
            self.checkNumberOperand(expr.operator, left, right)
            return float(left) > float(right)
        elif optype == TokenType.GREATER_EQUAL:
            self.checkNumberOperand(expr.operator, left, right)
            return float(left) >= float(right)
        elif optype == TokenType.LESS:
            self.checkNumberOperand(expr.operator, left, right)
            return float(left) < float(right)
        elif optype == TokenType.LESS_EQUAL:
            self.checkNumberOperand(expr.operator, left, right)
            return float(left) <= float(right)
        elif optype == TokenType.MINUS:
            return float(left) - float(right)
        elif optype == TokenType.PLUS:  # REVIEW: 对于 + 运算符，动态检测出操作数的类型并选择合适的操作
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)  # 数学运算
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)  # 连接字符串
            raise LoxRuntimeError(expr.operator, "Operator adds must be two number or two string.")
        elif optype == TokenType.SLASH:
            self.checkNumberOperand(expr.operator, left, right)
            return float(left) / float(right)
        elif optype == TokenType.STAR:
            self.checkNumberOperand(expr.operator, left, right)
            return float(left) * float(right)

        # Unreachable
        return None

    def evaluate(self, expr: Expr.Expr):
        """deliver the overriding visitor to expression#accept()"""
        return expr.accept(self)

    def excute(self, stmt: Stmt.Stmt):
        stmt.accept(self)

    def visitExpressionStmt(self, stmt: Stmt.Expression):
        self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self, stmt: Stmt.Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def isTruthy(self, obj: object) -> bool:
        """nil and false is truthy"""
        if obj == None: return False  # nil
        if isinstance(obj, bool): return bool(obj)
        return True

    def isEqual(self, a: object, b: object):
        # nil is only equal to nil
        if a is None and b is None: return True
        if a is None: return False

        return a.__eq__(b)

    def stringify(self, obj: object):
        if obj == None: return 'nil'

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith('.0'):
                return text[0:len(text) - 2]  # REVIEW: 不要误用 rstrip，会导致末尾的 0 丢失

        return str(obj)

    def interpreter(self, statements: List[Stmt.Stmt]):
        try:
            for statement in statements:
                self.excute(statement)
        except LoxRuntimeError as error:
            runtimeError(error)
