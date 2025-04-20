from abc import ABC

from .token import Token
from .expr import Expr

class Stmt(ABC):
    class Visitor(ABC):
        def visit_block_stmt(self, expr): raise NotImplementedError()
        def visit_expression_stmt(self, expr): raise NotImplementedError()
        def visit_print_stmt(self, expr): raise NotImplementedError()
        def visit_if_stmt(self, expr): raise NotImplementedError()
        def visit_var_stmt(self, expr): raise NotImplementedError()
        def visit_while_stmt(self, expr): raise NotImplementedError()
        def visit_for_stmt(self, expr): raise NotImplementedError()

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

class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        super().__init__()    
    
    def accept(self, visitor: Stmt.Visitor):
        return visitor.visit_if_stmt(self)

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

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor: Stmt.Visitor):
        return visitor.visit_while_stmt(self)

# class For(Stmt):
