from .expr import Expr, Binary, Unary, Literal, Grouping
from .token import Token
from .token_type import TokenType
from typing import Any

class Interpreter(Expr.Visitor):
    class RuntimeError(Exception):
        pass

    def interpret(self, expression: Expr):
        # try:
        value = self.evaluate(expression)
        print(self.stringify(value))
        # except Run

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
                raise self.RuntimeError(f"{expr} Operands must be two numbers or two strings.") 
        if T == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        if T == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        return None

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


    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def evaluate(self, expr: Grouping) -> Expr:
        return expr.accept(self)

    def is_truthy(self, ob):
        # TODO: check this is true in pythonx
        if ob is None:
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