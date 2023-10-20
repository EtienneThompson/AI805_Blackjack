"""Represents the game tree for a blackjack move."""
from EtienneAgentTree import DecisionNode, RandomNode, BaseNode


class GameTree:
    """Represents the game tree for a blackjack move."""

    def __init__(self, cards):
        # Change this to generate deeper game trees (more sequences of moves)
        self.max_depth = 4
        self._cards = cards
        self.root = BaseNode.BaseNode(self._cards)
        self.generate_game_tree(self.root, 0)

    def generate_game_tree(self, node, depth):
        """Recursively generate the game tree from the current state."""
        if depth >= self.max_depth:
            return

        possible_decisions = ["STAND", "HIT", "DOUBLE_DOWN", "SPLIT"]
        possible_ranks = ["2", "3", "4", "5", "6",
                          "7", "8", "9", "10", "J", "Q", "K", "A"]

        if depth % 2 == 0:
            print("Adding decision nodes...")
            # Decision tree node
            if node.get_hand_value() < 21:
                for decision in possible_decisions:
                    decision = DecisionNode.DecisionNode(
                        node.get_cards(), decision)
                    node.add_child(decision)

                    self.generate_game_tree(decision, depth + 1)

        if depth % 2 == 1:
            # Chance tree node
            print("Adding random nodes...")

            if (
                node.can_have_chance_nodes() and
                node.get_hand_value() < 21
            ):
                for rank in possible_ranks:
                    random = RandomNode.RandomNode(
                        node.get_cards(), rank + "♥")
                    node.add_child(random)

                    self.generate_game_tree(random, depth + 1)

    def get_leaf_nodes(self, node):
        """Return all the leaf nodes of the tree."""
        leaves = list()

        # Recursive base case to return the current node if it is a leaf.
        if (len(node.get_children()) == 0):
            return [node]

        # Append the leaf nodes of all children together.
        for child in node.children:
            leaves += self.get_leaf_nodes(child)

        return leaves

    def print_tree(self):
        """Print the tree to the console."""
        output = list()
        self._generate_output_for_node(self.root, output, 0)

        for depth in output:
            for node in depth:
                print(str(node) + "\t", end="")

            print("")

    def _generate_output_for_node(self, node, output, depth):
        """Helper method for printing the tree."""
        if (len(output) == depth):
            output.append(list())

        output[depth].append(node)

        for child in node.get_children():
            self._generate_output_for_node(child, output, depth + 1)
