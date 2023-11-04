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

    def get_node_weight(self):
        base_node_weight = super().get_node_weight()
        if self.type == "STAND":
            # Because everything else is the product of probabilities, if we use
            # the base weight for the STAND node, then it will always be the only
            # decision made. Instead, scale the decision based on how close
            # the hand is to 21
            return 2 * base_node_weight - 25

        return base_node_weight

    def __str__(self):
        return "Decision " + self.type + " " + str(self.get_cards())
