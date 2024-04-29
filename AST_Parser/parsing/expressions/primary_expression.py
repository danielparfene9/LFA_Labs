from math import floor, ceil
from ..node import Node, PrimaryNode

class PrimaryExpression(Node):
    def __init__(self, left, expression, right):
        self.left = left
        self.expression = expression
        self.right = right

    def nodes(self):
        return [self.left, self.expression, self.right]

    @classmethod
    def construct(cls, parser):
        if not parser.next().has("(", "|", "_", "^"):
            return Number.construct(parser)

        left = parser.take()
        expression = parser.expression.construct(parser)
        right = parser.expecting_has(")" if left.has("(") else left.string)

        return PrimaryExpression(left, expression, right)

    def interpret(self):
        value = self.expression.interpret()

        match self.left.string:
            case "(":
                return value
            case "|":
                return abs(value)
            case "_":
                return floor(value)
            case "^":
                return ceil(value)


class Number(PrimaryNode):
    @classmethod
    def construct(cls, parser):
        return Number(parser.expecting_of("Number"))

    def interpret(self):
        return (float if "." in self.token.string else int)(self.token.string)
