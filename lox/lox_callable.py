import time
# from lox.interpreter import Interpreter 

class LoxCallable:

    # def call(interpreter: Interpreter, arguments: list):
    def arity() -> int:
        return 0
    
    def call(interpreter, arguments: list):
        pass

    def __str__(self):
        return "<native fn>"


class Clock(LoxCallable):
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<native fn>"
