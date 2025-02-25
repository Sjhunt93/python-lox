import sys

from .scanner import Scanner

class Lox:

    had_error = False

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
            raise RuntimeError("..")

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

if __name__ == "__main__":
    Lox.main()