import sys

from lox.scanner import Scanner
from lox.parser import Parser
from lox.expr import AstPrinter
from lox.interpreter import Interpreter

class Lox:

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
        for t in tokens:
            print(t)

        parser = Parser(tokens)
        expr = parser.parse()
        if Lox.had_error:
            return
        print(AstPrinter()._print(expr))
        
        interpreter = Interpreter()
        interpreter.interpret(expr)
        


        
        
# chapter 7
#           static void runtimeError(RuntimeError error) {
#     System.err.println(error.getMessage() +
#         "\n[line " + error.token.line + "]");
#     hadRuntimeError = true;
#   }

# from chapter 5/6
#   private void synchronize() {
#     advance();

#     while (!isAtEnd()) {
#       if (previous().type == SEMICOLON) return;

#       switch (peek().type) {
#         case CLASS:
#         case FUN:
#         case VAR:
#         case FOR:
#         case IF:
#         case WHILE:
#         case PRINT:
#         case RETURN:
#           return;
#       }

#       advance();
#     }
#   }

if __name__ == "__main__":
    Lox.main()