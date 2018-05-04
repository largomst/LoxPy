from typing import List, Type

import Lox
from Expr import *
from Tokens import TokenType, Token


class ParseError(Exception):
    pass


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

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)

        self.error(self.peek(), "Except expression.")

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

    # REVIEW: 这里没有将 error 写到 Lox 中，并在这里导入了 Lox.report
    def error(self, token: Token, message: str) -> Type[ParseError]:
        if token.type == TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, " at '" + token.lexeme + "'", message)
        return ParseError

    def sychronize(self) -> None:
        self.advance()

        while self.isAtEnd():
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

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None
