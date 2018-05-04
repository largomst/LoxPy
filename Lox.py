import sys
from typing import TypeVar

# static check
import Interpreter
from Scanner import Scanner
import Parser

T = TypeVar('T')

interpreter = Interpreter.Interpreter()  # REVIEW: keep REPL session
hadError = False
hadRuntimeError = False


def main():
    if len(sys.argv) > 2:
        print('Usage: plox [script]')
    elif len(sys.argv) == 2:
        runFile(sys.argv[1])
    else:
        runPrompt()


def runFile(path: str):
    run(open(path, 'r', encoding='utf-8').read())
    if hadError: sys.exit(65)
    if hadRuntimeError: sys.exit(70)


def runPrompt():
    while True:
        run(input('> '))
        global hadError
        hadError = False


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    # for token in tokens:
    #     print(token)
    parser = Parser.Parser(tokens)
    expression = parser.parse()

    if hadError: return

    interpreter.interpreter(expression)


# Map<String, TokenType>

if __name__ == '__main__':
    main()
