from abc import ABC

from .token import Token

class Expr(ABC):
    class Visitor(ABC):
        def visit_assign_expr(self, expr: "Assign"): raise NotImplementedError()
        def visit_binary_expr(self, expr): raise NotImplementedError()
        def visit_call_expr(self, expr): raise NotImplementedError()
        def visit_get_expr(self, expr): raise NotImplementedError()
        def visit_grouping_expr(self, expr): raise NotImplementedError()
        def visit_literal_expr(self, expr): raise NotImplementedError()
        def visit_logical_expr(self, expr): raise NotImplementedError()
        def visit_set_expr(self, expr): raise NotImplementedError()
        def visit_super_expr(self, expr): raise NotImplementedError()
        def visit_this_expr(self, expr): raise NotImplementedError()
        def visit_unary_expr(self, expr): raise NotImplementedError()
        def visit_var_expr(self, expr): raise NotImplementedError()

    def __init__(self):
        pass

    def accept(self, visitor: Visitor):
        pass


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value
    
    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_assign_expr(self)

class Binary(Expr):

    def __init__(self, left: Expr, op: Token, right: Expr):
        self.left = left
        self.op = op
        self.right = right
    
    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_binary_expr(self)

class Unary(Expr):

    def __init__(self, op: Token, right: Expr):
        self.op = op
        self.right = right
    
    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_unary_expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_var_expr(self)


class AstPrinter(Expr.Visitor):
    def _print(self, expr: Expr):
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.op.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.op.lexeme, expr.right)

    def visit_literal_expr(self, expr: Literal):
        if not expr.value:
            return 'nil'
        else:
            return str(expr.value)

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)


    def parenthesize(self, name: str, *exprs: "Expr") -> str:
        builder = ["(", name]  # Use a list for efficient string concatenation
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))  # Assuming `Expr` has `accept()`
        builder.append(")")

        return "".join(builder)  # Convert list to string efficiently