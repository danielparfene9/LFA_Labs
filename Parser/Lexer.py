import re
from enum import Enum


class TokenType(Enum):
    NUMBER = r'\d+'
    STRING = r'"[^"]*"'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NEW = r'new'
    MODEL = r'model'
    BOOLEAN = r'(true|false)'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r','
    SEMI = r';'
    DOT = r'\.'
    WHITESPACE = r'\s+'
    EOF = r'$'

    def __init__(self, pattern):
        self.regex = re.compile(pattern)


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type.name}, {self.value})'

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = list(TokenType)
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            for token_type in self.tokens:
                match = token_type.regex.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    self.pos = match.end()

                    if token_type != TokenType.IDENTIFIER:
                        return Token(token_type, value)
                    else:
                        return Token(TokenType.IDENTIFIER, value)

            self.error()

        return Token(TokenType.EOF)
