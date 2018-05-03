from enum import Enum, auto


class TokenType(Enum):
    # Single - character
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE = [auto()] * 4
    COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR = [auto()] * 7

    # One or two character tokens.
    BANG, BANG_EQUAL = [auto()] * 2
    EQUAL, EQUAL_EQUAL = [auto()] * 2
    GREATER, GREATER_EQUAL = [auto()] * 2
    LESS, LESS_EQUAL, = [auto()] * 2

    # Literals.
    IDENTIFIER, STRING, NUMBER, = [auto()] * 3

    # Keywords.
    AND, CLASS, ELSE, FALSE, FUN, FOR, IF, NIL, OR, = [auto()] * 9
    PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE, = [auto()] * 7

    EOF = auto()


class Token:

    def __init__(self, type: TokenType, lexeme: str, literal: "Object", line: int):
        self.type, self.lexeme, self.literal, self.line = type, lexeme, literal, line

    def __str__(self):
        return '%s %s %s' % (self.type, self.lexeme, self.literal)

    def __repr__(self):
        args = f'{self.type}, {self.lexeme}, {self.literal}, {self.line}'
        return f'{self.__class__.__name__}({args})'
