"""Blackjack agent created by Etienne."""
from BaseAgent import BaseAgent
from EtienneAgentTree import GameTree
import Enums


class EtienneAgent(BaseAgent):
    def __init__(self, name: str, is_debug: bool):
        super().__init__(name, is_debug)
        self.total_traversed_nodes = 0
        self.max_traversed_nodes = 0

    # def place_bet(self):
    #     bet_value = 0
    #     if self._chips >= 2000:
    #         bet_value = 200
    #         self._bets.append(bet_value)
    #     elif self._chips > 1000:
    #         bet_value = 100
    #     else:
    #         bet_value = min(self._chips, 50)

    #     self._bets.append(bet_value)
    #     self._chips -= bet_value

    """
    Runs an expecti-minimax algorithm to determine an optimal move given the
    agent's current hand and knowledge of the game.
    """
    def run_agent(self, hand):
        """
        Constructs a game tree with random nodes, and runs the expect-minimax
        algorithm over the game tree to find the optimal move.
        """
        self.wait_for_user_input()

        game_tree = GameTree.GameTree(self._hands[hand], self._debug)
        # game_tree.print_tree()

        # self.wait_for_user_input()

        decision = game_tree.make_decision()
        # self.debug(decision)

        traversed_nodes = game_tree.get_traversed_nodes()
        self.total_traversed_nodes += traversed_nodes
        if traversed_nodes > self.max_traversed_nodes:
            self.max_traversed_nodes = traversed_nodes

        self._statuses[hand] = Enums.AgentStates[decision[0]]
        return self._statuses[hand]
