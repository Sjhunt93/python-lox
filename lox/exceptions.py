
from .token import Token
from .token_type import TokenType

# class Error(Exception):
#     def __init__(self, token: Token, msg: str):
def error_report(token: Token, msg: str):
    if token.type  == TokenType.EOF:
        print(f"{token.line} at end {msg}")
    else:
        print(f"{token.line} at {token.lexeme} {msg}")
