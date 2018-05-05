from typing import List

from Expr import *
from ParserError import ParseError
from Stmt import *
from Tokens import TokenType, Token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    # expression -> equality ;
    def expression(self) -> Expr:
        return self.equality()

    # equality -> comparison ( ( "!=" | "==" ) comparison )* ;
    def equality(self) -> Expr:
        expr = self.comparison()

        # 循环相当于 * 的作用，对于 match()  , 相当于 |
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    # comparison -> addition ( ( ">" | ">=" | "<" | "<=" ) addition )* ;
    def comparison(self) -> Expr:
        expr = self.addition()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.addition()
            expr = Binary(expr, operator, right)

        return expr

    # addition -> multiplication (("-"|"+") multiplication)*;
    def addition(self) -> Expr:
        expr = self.multiplication()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.multiplication()
            expr = Binary(expr, operator, right)

        return expr

    # multiplication -> unary (("/"|"*") unary)*;
    def multiplication(self) -> Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    # unary -> ("!" | "-"); unary | primary;
    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        else:
            return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)

        raise self.error(self.peek(), "Except expression.")

    # infrastructure primitive operation
    def match(self, *types: TokenType) -> bool:
        """checking to see if the current token is any of the given types"""

        # 只要有一个匹配就返回真
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        else:
            raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        err = ParseError(token, message)
        err.report()
        return err

    def check(self, tokenType: TokenType) -> bool:
        if self.isAtEnd(): return False  # REVIEW: 注意此处是否定
        return self.peek().type == tokenType  # REVIEW: 再次注意 match 和 peek 的区别，match 通过 advance 消耗 token

    def advance(self) -> Token:
        if not self.isAtEnd(): self.current += 1
        return self.previous()

    def isAtEnd(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def sychronize(self) -> None:
        self.advance()

        while not self.isAtEnd():  # REVIEW: 不止一次忘记的 not
            if self.previous().type == TokenType.SEMICOLON: return

            if self.peek().type in [TokenType.CLASS,
                                    TokenType.FUN,
                                    TokenType.VAR,
                                    TokenType.FUN,
                                    TokenType.IF,
                                    TokenType.WHILE,
                                    TokenType.PRINT,
                                    TokenType.RETURN]:
                return
        self.advance()

    def parse(self) -> List[Stmt]:
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())

        return statements

    def statement(self) -> Stmt:
        if (self.match(TokenType.PRINT)): return self.printStatement()
        if (self.match(TokenType.LEFT_BRACE)): return Block(self.block())
        return self.expressionStatement()

    def printStatement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Except ';' after value.")
        return Print(value)

    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Except ';' after expression.")
        return Expression(expr)

    def block(self) -> List[Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Except '}' after block.")
        return statements

    def assignment(self):
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self.error(equals, "Invalid assignment target.")

        return expr

    def declaration(self):
        try:
            if self.match(TokenType.VAR): return self.VarDeclaration()
            return self.statement()
        except ParseError as error:
            self.sychronize()
            return None

    def VarDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Except variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expcet ';' after variable declaration")
        return Var(name, initializer)
