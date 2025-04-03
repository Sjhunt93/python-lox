from .token import Token
from .token_type import TokenType
from .expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical
from .stmt import Stmt, Print, Expression, Var, Block, If
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
            statements.append(self.declaration())
        return statements
    
    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            else:
                return self.statement()
        except self.ParserError:
            #synchronize()
            pass
            return None

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.IF):
            return self.if_statement()

        if self.match(TokenType.PRINT):
            return self.print_statement()
        elif self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        else:
            return self.expression_statement()
    
    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return If(condition=condition, then_branch=then_branch, else_branch=else_branch)

#     return new Stmt.If(condition, thenBranch, elseBranch);



    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(expr)
    
    def block(self) -> list[Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")

        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        # expr = self.equality()
        expr = self.orr()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name , value)

            self.error(equals, "Invalid assignment type")

        return expr
    
    def orr(self) -> Expr:
        expr = self.andd()

        while self.match(TokenType.OR):
            op = self.previous()
            right = self.andd()
            expr = Logical(expr, op, right)

        return expr

    def andd(self) -> Expr:
        expr = self.equality()

        while self.match(TokenType.AND):
            op = self.previous()
            right = self.equality()
            expr = Logical(expr, op, right)

        return expr
    
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

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

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
    
