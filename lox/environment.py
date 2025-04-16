
from typing import Any
from .token import Token

class Environment:

    class EnvException(Exception):
        pass

    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing: "Environment" = enclosing
    
    def define(self, name: str, value: Any):
        print(f"define: {name} = {value} : {self.enclosing}")
        self.values[name] = value
    
    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing: 
            return self.enclosing.get(name)
        else:
            raise self.EnvException(f" {name} Undefined variable {name.lexeme} .")

    def assign(self, name: Token, value: Any):
        print(f"assign: {name.lexeme} = {value} : {self.enclosing}")
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif self.enclosing: 
            self.enclosing.assign(name, value)
        else:
            raise self.EnvException(f" {name} Undefined variable {name.lexeme} .")