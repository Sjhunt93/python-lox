from abc import ABC

from .token import Token
from .expr import Expr

class Stmt(ABC):
    class Visitor(ABC):
        def visit_block_stmt(self, expr): raise NotImplementedError()
        def visit_expression_stmt(self, expr): raise NotImplementedError()
        def visit_print_stmt(self, expr): raise NotImplementedError()
        def visit_var_stmt(self, expr): raise NotImplementedError()

    def __init__(self):
        pass

    def accept(self, visitor: Visitor):
        pass

class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: Stmt.Visitor):
        return visitor.visit_block_stmt(self)    

class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expression = expr
    
    def accept(self, visitor: Stmt.Visitor):
        return visitor.visit_expression_stmt(self)
    

class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expression = expr
    
    def accept(self, visitor: Stmt.Visitor):
        return visitor.visit_print_stmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: Stmt.Visitor):
        return visitor.visit_var_stmt(self)
