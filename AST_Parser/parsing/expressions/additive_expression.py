from .multiplicative_expression import MultiplicativeExpression
from ..node import BinaryNode


class AdditiveExpression(BinaryNode):
    @classmethod
    def construct(cls, parser):
        return cls.construct_binary(parser, cls, MultiplicativeExpression, ["+", "-"])

    def interpret(self):
        left = self.left.interpret()
        right = self.right.interpret()

        return left - right if self.op.has("-") else left + right
