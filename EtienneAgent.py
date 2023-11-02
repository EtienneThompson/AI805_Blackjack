"""Blackjack agent created by Etienne."""
from BaseAgent import BaseAgent
from EtienneAgentTree import GameTree
import Enums


class EtienneAgent(BaseAgent):
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

        self.wait_for_user_input()

        decision = game_tree.make_decision()
        self.debug(decision)

        self._statuses[hand] = Enums.AgentStates[decision[0]]
        return self._statuses[hand]
