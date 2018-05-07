from enum import Enum, auto
from typing import List, overload, Dict

from Expr import *
from ParserError import ParseError
from Stmt import *
import Interpreter
from Tokens import Token


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter: Interpreter.Interpreter):
        self.interpreter = interpreter
        self.scopes: List[Dict[str, bool]] = []  # 为什么变量是布尔值？
        self.currentFunction = FunctionType.NONE

    def resolveFunction(self, function_: Function, tpye: FunctionType):
        enclosingFunction = self.currentFunction
        self.currentFunction = type
        self.beginScope()
        for param in function_.parameters:
            self.declare(param)
            self.define(param)

        self.resolve(function_.body)
        self.endScope()
        self.currentFunction = enclosingFunction

    def visitBlockStmt(self, stmt: Block):
        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()
        return None

    def visitExpressionStmt(self, stmt: Expression):
        self.resolve(stmt.expression)
        return None

    def visitFunctionStmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolveFunction(stmt, FunctionType.FUNCTION)
        return None

    def visitIfStmt(self, stmt: If):
        """resolve all without control flow"""
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch is not None:
            self.resolve(stmt.elseBranch)
        return None

    def visitPrintStmt(self, stmt: Print):
        self.resolve(stmt.expression)
        return None

    def visitReturnStmt(self, stmt: Return):
        if self.currentFunction == FunctionType.NONE:
            ParseError(stmt.keyword, "Cannot return from top-level code.").report()

        if stmt.value is not None:
            self.resolve(stmt.value)

        return None

    def visitWhileStmt(self, stmt: While):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    def visitVarStmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)
        return None

    def visitAssignExpr(self, expr: Assign):
        self.resolve(expr.value)
        self.resolveLocal(expr, expr.name)
        return None

    def visitBinaryExpr(self, expr: Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visitCallExpr(self, expr: Call):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)
        return None

    def visitGroupingExpr(self, expr: Grouping):
        self.resolve(expr.expression)
        return None

    def visitLiteralExpr(self, expr: Literal):
        return None

    def visitLogicalExpr(self, expr: Logical):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visitUnaryExpr(self, expr: Unary):
        self.resolve(expr.right)
        return None

    def visitVariableExpr(self, expr: Variable):
        """if a variable is declared but not yet defined, report a error."""
        if not self.isEmpty(self.scopes) and self.peek(self.scopes).get(expr.name.lexeme) is False:
            ParseError(expr.name, "Cannot read local variable in its own initializer").report()

        self.resolveLocal(expr, expr.name)
        return None

    @overload
    def resolve(self, statements: List[Stmt]):
        """traverses into the statements inside the block and then discards the scope."""
        for statement in statements:
            self.resolve(statement)

    @overload
    def resolve(self, stmt: Stmt):
        stmt.accept(self)

    @overload
    def resolve(self, expr: Expr):
        expr.accept(self)

    def resolve(self, anyone):
        if isinstance(anyone, list):
            for anyone in anyone:
                self.resolve(anyone)
        elif isinstance(anyone, Stmt):
            anyone.accept(self)
        elif isinstance(anyone, Expr):
            anyone.accept(self)

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        """make the variable as not ready yet by binding its name to false in the scope"""
        if self.isEmpty(self.scopes): return
        scope: Dict = self.peek(self.scopes)

        if name.lexeme in scope.keys():
            ParseError(name, "Variable with the name already declared in the scope.").report()

        scope[name.lexeme] = False

    def isEmpty(self, l: list):
        return len(l) == 0

    def peek(self, l: list):
        return l[-1]

    def define(self, name: Token):
        if self.isEmpty(self.scopes): return
        self.peek(self.scopes)[name.lexeme] = True

    def resolveLocal(self, expr: Expr, name: Token):
        # for i in range(len(self.scopes) - 1, -1, -1):
        for i in reversed(range(len(self.scopes))):
            if name.lexeme in self.scopes[i].keys():
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
