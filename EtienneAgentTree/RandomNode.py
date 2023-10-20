"""Node representing a random card draw in the game tree."""
from EtienneAgentTree import BaseNode


class RandomNode(BaseNode.BaseNode):
    """Random specific implementation of a node in the game tree."""

    def __init__(self, hand, rank):
        super().__init__(hand)
        self._cards.append(rank)
        self.rank = rank

    def __str__(self):
        return "Random " + str(self.get_cards())
