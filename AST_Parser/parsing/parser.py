from AST_Parser.util.error import LanguageError
from .expressions.expression import Expression


class ParserError(LanguageError):
    pass


class Parser:
    @property
    def expression(self):
        return Expression

    def __init__(self):
        self.tokens = None
        self.i = -1

    def next(self):
        return self.tokens[self.i]

    def take(self):
        token = self.next()
        self.i += 1
        return token

    def expecting_has(self, *strings):
        if self.next().has(*strings):
            return self.take()

        raise ParserError(self.next(), f"Expecting has {strings}")

    def expecting_of(self, *kinds):
        if self.next().of(*kinds):
            return self.take()

        raise ParserError(self.next(), f"Expecting of {kinds}")

    def make_tree(self, tokens):
        self.tokens, self.i = tokens, 0
        node = Expression.construct(self)

        if self.next().has("EOF"):
            return node

        raise ParserError(self.next(), f"Unexpected token {self.next()}")
