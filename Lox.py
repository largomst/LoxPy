import sys
from typing import TypeVar

# static check
import Interpreter
import ErrorState
from Resolver import Resolver
from Scanner import Scanner
import Parser

ErrorState.hadError = False
ErrorState.hadRuntimeError = False
T = TypeVar('T')

interpreter = Interpreter.Interpreter()  # REVIEW: keep REPL session


def main():
    if len(sys.argv) > 2:
        print('Usage: plox [script]')
    elif len(sys.argv) == 2:
        runFile(sys.argv[1])
    else:
        runPrompt()


def runFile(path: str):
    run(open(path, 'r', encoding='utf-8').read())
    if ErrorState.hadError:
        sys.exit(65)
    if ErrorState.hadRuntimeError:
        sys.exit(70)


def runPrompt():
    nested = 0
    source = ""
    dollar = '>'

    while True:
        temp = input(dollar + ' ')
        source += temp
        for c in temp:
            if c == '(' or c == '{':
                nested += 1
            elif c == ')' or c == '}':
                nested -= 1
        if nested == 0:
            run(source)
            source = ""
            dollar = '> '
        else:
            dollar = ':'
        ErrorState.hadError = False


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    parser = Parser.Parser(tokens)
    statements = parser.parse()
    if ErrorState.hadError:
        return
    resolver = Resolver(interpreter)
    resolver.resolve(statements)

    # stop if there was a resolution error.
    if ErrorState.hadError:
        return

    interpreter.interpreter(statements)


# Map<String, TokenType>

if __name__ == '__main__':
    main()
