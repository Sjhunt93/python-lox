
from typing import Any
from .token import Token

class Environment:

    class EnvException(Exception):
        pass

    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing: "Environment" = enclosing
    
    def define(self, name: str, value: Any):
        # print(f"define: {name} = {value} : {self.enclosing}")
        self.values[name] = value
    
    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing: 
            return self.enclosing.get(name)
        else:
            raise self.EnvException(f" {name} Undefined variable {name.lexeme} .")

    def get_at(self, distance: int, name: str):
        return self.ancestor(distance).values[name]

    def assign_at(self, distance: int, name: Token, value: Any):
        self.ancestor(distance).values[name] = value

    def assign(self, name: Token, value: Any):
        # print(f"assign: {name.lexeme} = {value} : {self.enclosing}")
        print(f"Looking up '{name.lexeme}' in {self.values}")

        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif self.enclosing: 
            self.enclosing.assign(name, value)
        else:
            raise self.EnvException(f" {name} Undefined variable {name.lexeme} .")
    
    def ancestor(self, distance: int) -> "Environment":
        env = self
        for i in range(distance):
            env = env.enclosing
        return env