"""Represents a basic node in the game tree."""
import card_methods


class BaseNode:
    """Common implementation between various tree nodes."""

    def __init__(self, cards):
        self._cards = cards
        self.children = list()
        self.weight = 0

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
