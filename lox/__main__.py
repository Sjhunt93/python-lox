import sys

from lox.scanner import Scanner
from lox.parser import Parser
from lox.expr import AstPrinter
from lox.interpreter import Interpreter
from lox.resolver import Resolver

class Lox:

    interpreter = Interpreter()
    had_error = False
    had_runtime_error = False

    @staticmethod
    def error(line, message):
        Lox.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Lox.had_error = True

    @staticmethod
    def main():
        Lox.run_file("hello.lox")
        if len(sys.argv) > 2:
            print("Usage: lox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Lox.run_file(sys.argv[1])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(filename):
        with open(filename, "r") as file:
            Lox.run(file.read())
        if Lox.had_error:
            sys.exit(65)
        if Lox.had_runtime_error:
            sys.exit(70)

    @staticmethod
    def run_prompt():
        while True:
            try:
                line = input("> ")
                if not line:
                    break
                Lox.run(line)
                Lox.had_error = False
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break

    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        # for t in tokens:
        #     print(t)

        parser = Parser(tokens)
        statements = parser.parse()
        if Lox.had_error:
            return
        
        # print(AstPrinter()._print(statements))
        
        resolver = Resolver(Lox.interpreter)
        resolver.resolve(statements)
        
        if Lox.had_error:
            return
        
        r = Lox.interpreter.interpret(statements)
        if r:
            print(r)
        

if __name__ == "__main__":
    Lox.main()