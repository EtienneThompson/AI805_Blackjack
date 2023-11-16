"""Represents a basic node in the game tree."""
import card_methods


class BaseNode:
    """Common implementation between various tree nodes."""

    def __init__(self, cards):
        self._cards = cards
        self.children = list()

    def get_children(self):
        """Returns all the children of this node."""
        return self.children

    def add_child(self, child_node):
        """Adds a node to the game tree."""
        if not isinstance(child_node, BaseNode):
            return

        self.children.append(child_node)

    def get_cards(self):
        """Returns a copy of the cards in the node."""
        return [] + self._cards

    def get_hand_value(self):
        """Computes the value of the cards in the hand."""
        return card_methods.calculate_hand_value(self._cards)

    def get_node_weight(self, reverse_weight=False):
        """Computes weight of node based on hand value"""
        hand_value = self.get_hand_value()
        if hand_value <= 21:
            return hand_value if not reverse_weight else 0
        else:
            # Hands that have bust should not contribute to the probability of
            # a good move.
            return 0 if not reverse_weight else (hand_value - 21) * 2

    def __str__(self):
        return "Root"
