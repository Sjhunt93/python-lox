from abc import ABC

from .token import Token
from .expr import Expr

class Stmt(ABC):
    class Visitor(ABC):
        def visit_expression_stmt(self, expr): raise NotImplementedError()
        def visit_print_stmt(self, expr): raise NotImplementedError()

    def __init__(self):
        pass

    def accept(self, visitor: Visitor):
        pass

class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr
    
    def accept(self, visitor: Stmt.Visitor):
        return visitor.visit_expression_stmt(self)
    

class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr
    
    def accept(self, visitor: Stmt.Visitor):
        return visitor.visit_print_stmt(self)
