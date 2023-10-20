"""Node representing a random card draw in the game tree."""
from EtienneAgentTree import BaseNode


class RandomNode(BaseNode.BaseNode):
    """Random specific implementation of a node in the game tree."""

    def __init__(self, hand, rank):
        super().__init__(hand)
        self.rank = rank
