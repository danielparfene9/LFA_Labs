from abc import ABC
from .additive_expression import AdditiveExpression
from ..node import Node


class Expression(Node, ABC):
    @classmethod
    def construct(cls, parser):
        return AdditiveExpression.construct(parser)
