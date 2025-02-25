from lox.expr import *
from lox.token_type import TokenType

# T = Token(TokenType.MINUS, "-", None, 1)
# expression = Binary(Unary(T, )

expression = Unary(Token(TokenType.MINUS, "-", None, 1), Literal(10))

AstPrinter()._print(expression)