"""Represents the game tree for a blackjack move."""
from EtienneAgentTree import DecisionNode, RandomNode, BaseNode
import card_methods


class GameTree:
    """Represents the game tree for a blackjack move."""

    def __init__(self, cards, is_debug):
        self.is_debug = is_debug
        # Change this to generate deeper game trees (more sequences of moves)
        self.max_depth = 4
        self._cards = cards
        self.root = BaseNode.BaseNode(self._cards)
        self.generate_game_tree(self.root, 0)

        self.traversed_nodes = 0

    def generate_game_tree(self, node, depth):
        """Recursively generate the game tree from the current state."""
        if depth >= self.max_depth:
            return

        possible_decisions = ["STAND", "HIT", "DOUBLE_DOWN"]
        possible_ranks = ["2", "3", "4", "5", "6",
                          "7", "8", "9", "10", "J", "Q", "K", "A"]

        if depth % 2 == 0:
            # self._debug("Adding decision nodes...")
            # Decision tree node
            if node.get_hand_value() < 21:
                if card_methods.can_split_hand(node.get_cards()):
                    possible_decisions.append("SPLIT")
                for decision in possible_decisions:
                    decision = DecisionNode.DecisionNode(
                        node.get_cards(), decision)
                    node.add_child(decision)

                    self.generate_game_tree(decision, depth + 1)

        if depth % 2 == 1:
            # Chance tree node
            # self._debug("Adding random nodes...")

            if node.get_hand_value() < 21:
                for rank in possible_ranks:
                    # self._debug(
                    #     f"node type: {node.type} - is final decision: {node.is_final_decision()}")
                    random = RandomNode.RandomNode(
                        node.get_cards(), rank + "♥", 1 / 13, node.is_final_decision())
                    node.add_child(random)

                    self.generate_game_tree(random, depth + 1)

    def get_leaf_nodes(self, node):
        """Return all the leaf nodes of the tree."""
        leaves = list()

        # Recursive base case to return the current node if it is a leaf.
        if len(node.get_children()) == 0:
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
                self._debug(str(node) + "\t", end="")

            self._debug("")

    def make_decision(self):
        """Wrapper method for expeci-minimax algorithm method."""
        decision, weight = self._expectminimax(self.root, 0)
        print(f"Expectiminimax traversed {self.traversed_nodes} nodes")
        return [decision, weight]

    def _expectminimax(self, node, depth):
        self.traversed_nodes += 1
        """Recursively computes the best move given the game tree rooted at node."""
        if len(node.get_children()) == 0:
            if isinstance(node, DecisionNode.DecisionNode):
                # self._debug(
                #     f"Decision node leaf at depth {depth}: {node.type}, {node.get_node_weight()}")
                return [node.type, node.get_node_weight()]
            elif isinstance(node, RandomNode.RandomNode):
                # Since it's a random node, the decision will be made in the parent node.
                # self._debug(
                #     f"Random node leaf at depth {depth}: \"\", is_final_chance node: {node.is_final_chance()}, {node.get_node_weight(reverse_weight=node.is_final_chance())}, card: {node.get_cards()}")
                return ["", node.get_node_weight(reverse_weight=node.is_final_chance())]
            else:
                # This happens when we have no decision tree because we have a 21
                # in our hand already.
                return ["STAND", 21]

        if isinstance(node, DecisionNode.DecisionNode):
            weight = 0
            # self._debug(
            #     f"Checking weight for decision node at depth {depth}: {node.type}")
            for child in node.get_children():
                _, value = self._expectminimax(child, depth+1)
                weight += child.probability * value
            # self._debug(
            #     f"Decision Node at depth {depth}: {node.type}, {weight}")
            return [node.type, weight]
        elif isinstance(node, RandomNode.RandomNode) or isinstance(node, BaseNode.BaseNode):
            options = list()
            for child in node.get_children():
                options.append(self._expectminimax(child, depth+1))
            max_node = max(options, key=lambda x: x[1])
            # self._debug(
            #     f"Random Node at depth {depth}: {max_node[0]}, {max_node[1]}")
            return max_node

        # This case shouldn't happen, but just have a fallback in case.
        # self._debug("Fallback case")
        return ["", node.get_node_weight()]

    def _generate_output_for_node(self, node, output, depth):
        """Helper method for printing the tree."""
        if len(output) == depth:
            output.append(list())

        output[depth].append(node)

        for child in node.get_children():
            self._generate_output_for_node(child, output, depth + 1)

    def _debug(self, data, end="\n"):
        if self.is_debug:
            print(data, end=end)
