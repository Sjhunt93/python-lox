from .lox_callable import LoxCallable
from .stmt import Function
from .environment import Environment

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration
    
    def call(self, interpreter, arguments: list):
        environment = Environment(interpreter._globals)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        interpreter.execute_block(self.declaration.body, environment)

    def arity(self):
        return len(self.declaration.params)
    
    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"
