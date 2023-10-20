"""Blackjack agent created by Etienne."""
import random
from BaseAgent import BaseAgent
from EtienneAgentTree import GameTree
import Enums


class EtienneAgent(BaseAgent):
    """
    Runs an expecti-minimax algorithm to determine an optimal move given the
    agent's current hand and knowledge of the game.
    """

    def run_agent(self):
        """
        Constructs a game tree with random nodes, and runs the expect-minimax
        algorithm over the game tree to find the optimal move.
        """
        self.wait_for_user_input()

        game_tree = GameTree.GameTree(self._cards)
        game_tree.print_tree()

        actions = [Enums.AgentStates.HIT, Enums.AgentStates.STAND]
        if self._bet * 2 <= self._chips:  # Check if the agent has enough chips to double down
            actions.append(Enums.AgentStates.DOUBLE_DOWN)
        if self.can_split():
            actions.append(Enums.AgentStates.SPLIT)

        self._status = random.choice(actions)

        if self._status == Enums.AgentStates.DOUBLE_DOWN:
            self._bet *= 2  # Double the bet
            self._chips -= self._bet  # Update the chips

        elif self._status == Enums.AgentStates.SPLIT:
            # Logic for splitting the cards into two hands
            pass  # Implement this part as per your game logic

        return self._status
