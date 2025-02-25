from lox.expr import *
from lox.token_type import TokenType

# T = Token(TokenType.MINUS, "-", None, 1)
# expression = Binary(Unary(T, )

expression = Unary(Token(TokenType.MINUS, "-", None, 1), Literal(10))

expression = Binary(
    Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(123)),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(
        Literal(45.67)
    )
)

print(AstPrinter()._print(expression))