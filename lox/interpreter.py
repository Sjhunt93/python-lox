from .expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical, Call
from .token import Token
from .token_type import TokenType
from typing import Any
from .stmt import Stmt, Print, Expression, Var, Block, If, While, Function, Return
from .environment import Environment
from .lox_callable import LoxCallable, Clock
from .lox_function import LoxFunction


class Interpreter(Expr.Visitor, Stmt.Visitor):
    class RuntimeError(Exception):
        pass

    class Return(Exception):
        def __init__(self, value):
            self.value = value
    
    def __init__(self):
        self._globals = Environment()
        self.environment = self._globals

        self._globals.define("clock", Clock())

    def interpret(self, statements: list[Stmt]):
        # try:
        try:
            r = 0
            for statement in statements:
                r = self.execute(statement)
            return r
        except Exception as e:
            raise self.RuntimeError(e)
    
    def execute(self, stmt: Stmt):
        return stmt.accept(self)
    
    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous: Environment = self.environment

        self.environment = environment
        try:
            for statement in statements:
                self.execute(statement)
        # horrid edge case
        finally:
            self.environment = previous



    def visit_block_stmt(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None


    def stringify(self, ob):
        if ob is None:
            return 'nil'
        elif isinstance(ob, float):
            text = str(ob)
            if text.endswith(".0"):
                text = text[0 : len(text) - 2]
            return text
        else:
            return str(ob)


    # ================================ Expr.Visitor ================================
    def visit_binary_expr(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        T = expr.op.type
        if T == TokenType.GREATER:
            self.check_number_operand_3(expr.op, left, right)
            return left > right
        if T == TokenType.GREATER_EQUAL:
            self.check_number_operand_3(expr.op, left, right)
            return left >= right
        if T == TokenType.LESS:
            self.check_number_operand_3(expr.op, left, right)
            return left < right
        if T == TokenType.LESS_EQUAL:
            self.check_number_operand_3(expr.op, left, right)
            return left <= right
        if T == TokenType.MINUS:
            self.check_number_operand_3(expr.op, left, right)
            return float(left) - float(right)
        if T == TokenType.SLASH:
            self.check_number_operand_3(expr.op, left, right)
            if right == 0.0:
                raise self.RuntimeError("Division by 0")
            return float(left) / float(right)
        if T == TokenType.STAR:
            self.check_number_operand_3(expr.op, left, right)
            return float(left) * float(right)
        if T == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            else:
                return str(left) + str(right)
                raise self.RuntimeError(f"{expr} Operands must be two numbers or two strings.") 
        if T == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        if T == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        return None

    def visit_call_expr(self, expr: Call):
        callee = self.evaluate(expr.callee)

        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))
        
        if not isinstance(callee, LoxCallable):
            raise self.RuntimeError("Can only call functions and classes.")
        
        function: LoxCallable = callee
        if len(arguments) != function.arity():
            raise self.RuntimeError("Expected " +
                function.arity() + " arguments but got " +
                len(arguments) + ".")

        return function.call(self, arguments)
        

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)
        T = expr.op.type
        if T == TokenType.MINUS:
            return -float(right)
        if T == TokenType.BANG:
            return not self.is_truthy(right)
        # should be unreachable
        return None

    def visit_literal_expr(self, expr: Literal):
        return expr.value
    
    def visit_logical_expr(self, expr: Logical):
        left = self.evaluate(expr.left)
        
        if expr.op.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        
        return self.evaluate(expr.right)
    
    def visit_while_stmt(self, stmt: While):
        
        while self.is_truthy(self.evaluate(stmt.condition)):
            
            self.execute(stmt.body)
        
        return None
    


#   @Override
#   public Object visitLogicalExpr(Expr.Logical expr) {
#     Object left = evaluate(expr.left);

#     if (expr.operator.type == TokenType.OR) {
#       if (isTruthy(left)) return left;
#     } else {
#       if (!isTruthy(left)) return left;
#     }

#     return evaluate(expr.right);
#   }

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def evaluate(self, expr: Grouping) -> Expr:
        return expr.accept(self)

    def is_truthy(self, ob):
        # TODO: check this is true in pythonx
        if ob is None:
            return False
        if ob == 0.0 or ob == 0:
            return False
        if isinstance(ob, bool):
            return bool(ob)
        else:
            return True
        
    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        elif a == None:
            return False
        else:
            return a == b

    def check_number_operand(self, op: Token, operand: Any):
        if isinstance(operand, float):
            return
        raise self.RuntimeError(f"{op} Operand must be a number.") 

    def check_number_operand_3(self, op: Token, left: Any, right: Any):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise self.RuntimeError(f"{op} Operands must be a number.") 
    

    # ================================ Stmt.Visitor ================================

    def visit_expression_stmt(self, stmt: Expression):
        return self.evaluate(stmt.expression)
    
    def visit_function_stmt(self, stmt: Function):
        function = LoxFunction(stmt)
        self.environment.define(stmt.name.lexeme, function)
        return None
    
    def visit_if_stmt(self, stmt: If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch != None:
            self.execute(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visit_return_stmt(self, stmt: Return):
        value = None
        if stmt.value != None:
            value = self.evaluate(stmt.value)
        raise self.Return(value)
    
    def visit_var_stmt(self, stmt: Var):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_var_expr(self, expr: Variable):
        return self.environment.get(expr.name)