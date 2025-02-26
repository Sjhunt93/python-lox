from .token import Token
from .token_type import TokenType
from .expr import Expr, Binary, Unary, Literal, Grouping
from .stmt import Stmt, Print, Expression
from .exceptions import error_report

class Parser:

    class ParserError(Exception):
        pass

    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements
    
    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        else:
            return self.expression_statement()
    
    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(expr)
    
    def expression(self) -> Expr:
        return self.equality()

    #equality --> comparison ( ( "!=" | "==" ) comparison )* ;
    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self.previous()
            right = self.comparison()
            expr = Binary(expr, op, right)
        
        return expr

    #comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            op = self.previous()
            right = self.term()
            expr = Binary(expr, op, right)

        return expr
        

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            op = self.previous()
            right = self.factor()
            expr = Binary(expr, op, right)
        
        return expr
    
    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            op = self.previous()
            right = self.unary()
            expr = Binary(expr, op, right)
        
        return expr
    
    # unary → ( "!" | "-" ) unary | primary ;
    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.unary()
            return Unary(op, right)
        else:
            return self.primary()
        
    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.ParserError(f"{self.peek()}, Expect expression")


    def consume(self, t: TokenType, message: str):
        if self.check(t):
            return self.advance()
        else:
            raise self.error(self.peek(), message)
    
    def error(self, token: Token, message: str):
        error_report(token, message)
        return self.ParserError("Could not parse")
    
    def match(self, * types: TokenType):
        for t in types:
            if self.check(t):
                self.advance()
                return True
      
        return False
    
    def check(self, t: TokenType):
        if self.is_at_end():
            return False
        return self.peek().type == t

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]
    
