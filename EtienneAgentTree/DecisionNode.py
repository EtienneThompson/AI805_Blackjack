"""Node representing a decision in the game tree."""
from EtienneAgentTree import BaseNode


class DecisionNode(BaseNode.BaseNode):
    """Decision specific implementation of a node in the tree."""

    def __init__(self, hand, node_type):
        super().__init__(hand)
        self.type = node_type

    def can_have_chance_nodes(self):
        """Determines if the node can have chance nodes."""
        return self.type == "HIT" or self.type == "DOUBLE_DOWN" or self.type == "SPLIT"

    def __str__(self):
        return "Decision " + self.type + " " + str(self.get_cards())
