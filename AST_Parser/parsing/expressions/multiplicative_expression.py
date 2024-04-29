from .exponential_expression import ExponentialExpression
from ..node import BinaryNode


class MultiplicativeExpression(BinaryNode):
    @classmethod
    def construct(cls, parser):
        return cls.construct_binary(parser, cls, ExponentialExpression, ["*", "/", "%"])

    def interpret(self):
        left = self.left.interpret()
        right = self.right.interpret()

        match self.op.string:
            case "*":
                return left * right
            case "/":
                return left / right
            case "%":
                return left % right
