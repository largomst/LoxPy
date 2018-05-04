# usr/bin env python3
# coding: utf-8
from typing import Type

import ScannerError
from Tokens import TokenType, Token


class ParseError(Exception):
    pass


def error(token: Token, message: str) -> Type[ParseError]:
    if token.type == TokenType.EOF:
        ScannerError.report(token.line, " at end", message)
    else:
        ScannerError.report(token.line, " at '" + token.lexeme + "'", message)
    return ParseError