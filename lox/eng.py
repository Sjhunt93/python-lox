import sys

from lox.scanner import Scanner
from lox.parser import Parser
from lox.expr import AstPrinter
from lox.interpreter import Interpreter

class Eng:

    interpreter = Interpreter()
    had_error = False
    had_runtime_error = False

    @staticmethod
    def error(line, message):
        Eng.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Eng.had_error = True

    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        # for t in tokens:
        #     print(t)

        parser = Parser(tokens)
        statements = parser.parse()
        if Eng.had_error:
            return
        
        # print(AstPrinter()._print(statements))
        
        return Eng.interpreter.interpret(statements)