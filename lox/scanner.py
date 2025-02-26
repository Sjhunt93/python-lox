
from .token_type import TokenType
from .token import Token

class Scanner:

    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    class Error(Exception):
        pass

    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens: list[Token] = []


    def is_at_end(self):
        return self.current >= len(self.source)
    
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def advance(self):
        self.current += 1
        return self.source[self.current-1]
    
    def add_token(self, ttype: TokenType, literal):
        t = self.source[self.start : self.current]
        self.tokens.append(Token(ttype, t, literal, self.line))

    def scan_token(self) -> None:
        def add_token(ttype: TokenType):
            self.add_token(ttype, None)

        c = self.advance()

        if c == '(':
            add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            add_token(TokenType.COMMA)
        elif c == '.':
            add_token(TokenType.DOT)
        elif c == '-':
            add_token(TokenType.MINUS)
        elif c == '+':
            add_token(TokenType.PLUS)
        elif c == ';':
            add_token(TokenType.SEMICOLON)
        elif c == '*':
            add_token(TokenType.STAR)
        # -----------------------
        elif c == '!':
            add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            # multi-line comment
            if self.match("*"):
                while self.peek() != '*' and not self.is_at_end() and self.peek_next() != '/':
                    self.advance()
                # need to skip over last /
                self.advance()
                self.advance()
            elif self.match("/"):
                # remove comments..
                while (self.peek() != '\n' and not self.is_at_end()):
                    self.advance()
            else:
                add_token(TokenType.SLASH)
        elif c in [' ', '\t', '\r']:
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.parse_string()
        elif c == 'o':
            if self.match('r'):
                add_token(TokenType.OR)
            
        else:
            if c.isdigit():
                self.parse_number()
            elif self.is_alpha(c):
                self.parse_identifier()
            else:
                raise self.Error(f"Unexpected character on: {self.line}")

        
    def is_alpha(self, c: str) -> bool:
        return c.isalpha() or c == '_'

    def is_alphanumeric(self, c: str) -> bool:
        return self.is_alpha(c) or c.isdigit()

    def parse_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise self.Error(f"Unterminated string on line {self.line}")
        
        self.advance()
        val = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, val)

    

    def parse_number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
        while self.peek().isdigit():
            self.advance()

        # PARSE as float for now
        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current ]))

    def parse_identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()
        
        t = self.source[self.start : self.current]
        token_type = self.KEYWORDS.get(t, TokenType.IDENTIFIER)
        self.add_token(token_type, None)

    def match(self, expected: str):
        if self.is_at_end():
            return False
        elif self.source[self.current] != expected:
            return False
        else:
            self.current += 1
            return True
  
    def peek(self):
        if self.is_at_end():
            return "\0"
        else:
            return self.source[self.current]
    
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        else:
            return self.source[self.current + 1]
#     if (isAtEnd()) return false;
#     if (source.charAt(current) != expected) return false;

#     current++;
#     return true;
#   }