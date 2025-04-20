import time
# from lox.interpreter import Interpreter 

class LoxCallable:

    # def call(interpreter: Interpreter, arguments: list):
    def arity(self) -> int:
        return 0
    
    def call(self, interpreter, arguments: list):
        pass

    def __str__(self):
        return "<native fn>"


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments: list):
        return time.time()

    def __str__(self):
        return "<native fn>"
