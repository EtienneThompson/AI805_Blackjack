"""Node representing a decision in the game tree."""
from EtienneAgentTree import BaseNode


class DecisionNode(BaseNode.BaseNode):
    """Decision specific implementation of a node in the tree."""

    def __init__(self, hand, node_type):
        super().__init__(hand)
        self.type = node_type

    def is_final_decision(self):
        return self.type == "DOUBLE_DOWN" or self.type == "STAND"

    def __str__(self):
        return "Decision " + self.type + " " + str(self.get_cards())
