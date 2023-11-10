"""Node representing a random card draw in the game tree."""
from EtienneAgentTree import BaseNode


class RandomNode(BaseNode.BaseNode):
    """Random specific implementation of a node in the game tree."""

    def __init__(self, hand, rank, probability, is_final):
        super().__init__(hand)
        self._cards.append(rank)
        self.rank = rank
        self.probability = probability
        self.is_final = is_final

    def is_final_chance(self):
        return self.is_final

    def __str__(self):
        return "Random " + str(self.get_cards()) + " " + str(self.probability)
