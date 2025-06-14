from .token import Token
from .token_type import TokenType, FunctionType

from .expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical, Call
from .stmt import Stmt, Print, Expression, Var, Block, If, While, Function, Return

class Resolver(Expr.Visitor, Stmt.Visitor):

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function: FunctionType = FunctionType.NONE
    
    def resolve_stmt_list(self, statements: list[Stmt]):
        for s in statements:
            self.resolve_stmt(s)

    def resolve_stmt(self, stmt: Stmt):
        stmt.accept(self)
    
    def resolve_expr(self, expr: Expr):
        expr.accept(self)
    

    def resolve(self, ob):
        # if isinstance(ob, list[Stmt]):
        if isinstance(ob, list) and isinstance(ob[0], Stmt):
            self.resolve_stmt_list(ob)
        if isinstance(ob, Stmt):
            self.resolve_stmt(ob)
        if isinstance(ob, Expr):
            self.resolve_expr(ob)

    def begin_scope(self):
        self.scopes.append({})
    
    def end_scope(self):
        self.scopes.pop()
    
    
    def visit_block_stmt(self, stmt: Block):
        self.begin_scope()
        self.resolve_stmt_list(stmt.statements)
        self.end_scope()
        return None

    def visit_var_stmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initializer:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)
        return None
    
    def visit_var_expr(self, expr: Variable):
         
        if len(self.scopes) and self.scopes[-1][expr.name.lexeme] == False:
            raise Exception(f"{expr.name} Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)
        return None
    
    def visit_assign_expr(self, expr: Assign):
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)
        return None
    
    def visit_function_stmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None

    def visit_expression_stmt(self, stmt: Expression):
        self.resolve(stmt.expression)
        return None
    
    def visit_if_stmt(self, stmt: If):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch:
            self.resolve(stmt.else_branch)
        return None
    
    def visit_print_stmt(self, stmt: Print):
        self.resolve(stmt.expression)
        return None
    
    def visit_return_stmt(self, stmt: Return):
        if self.current_function == FunctionType.NONE:
            raise Exception("Can't return from top-level code.")
        if stmt.value:
            self.resolve(stmt.value)
        return None
    
    def visit_while_stmt(self, stmt: While):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    def visit_binary_expr(self, expr: Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_call_expr(self, expr: Call):
        self.resolve(expr.callee)

        for argument in expr.arguments:
            self.resolve(argument)
        return None
    
    def visit_grouping_expr(self, expr: Grouping):
        self.resolve(expr.expression)
        return None
    
    def visit_literal_expr(self, expr):
        return None
    
    def visit_logical_expr(self, expr: Logical):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_unary_expr(self, expr: Unary):
        self.resolve(expr.right)
        return None
        

    
    # RESOLVERS
    def resolve_local(self, expr: Expr, name: Token):
        i = len(self.scopes) - 1
        while i >= 0:
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
            i -= 1

    def resolve_function(self, function: Function, ftype: FunctionType):
        enclosing_function = self.current_function
        self.current_function = ftype

        self.begin_scope()

        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve_stmt_list(function.body)
        self.end_scope()
        self.currentFunction = enclosing_function

    def declare(self, name: Token):
        if not self.scopes: 
            return
        
        scope: dict = self.scopes[-1]
        if name.lexeme in scope:
            raise Exception(f"Already a variable with this name '{name.lexeme}' in this scope.")

        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes: 
            return
        self.scopes[-1][name.lexeme] = True