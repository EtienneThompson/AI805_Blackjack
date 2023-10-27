import random
from BaseAgent import BaseAgent
import Enums
import card_methods


class KevinAgent(BaseAgent):
    DEFAULT_BET = 50  # This will be the default betting amount

    def place_bet(self, hand):  # this is new betting function
        """Decide how much to bet based on the current hand."""
        # Check if the hand contains an Ace or a 10-value card
        if "A" in self._hands[hand] or any(card[:-1] in ["10", "J", "Q", "K"] for card in self._hands[hand]):
            # Bet double the default amount, but not more than available chips
            return min(self._chips, self.DEFAULT_BET * 2)
        else:
            # Bet the default amount, but not more than available chips
            return min(self._chips, self.DEFAULT_BET)

    def run_agent(self, hand):
        self.wait_for_user_input()

        # At the start of the round the Agent decides how much to bet.
        self._bet = self.place_bet(hand)
        self._chips -= self._bet  # The agent deducts the bet amount from their total chips

        actions = [Enums.AgentStates.HIT, Enums.AgentStates.STAND]
        if self._bet * 2 <= self._chips:  # Check if the agent has enough chips to double down
            actions.append(Enums.AgentStates.DOUBLE_DOWN)
        if self.can_split(hand):
            # actions.append(Enums.AgentStates.SPLIT)
            actions = [Enums.AgentStates.SPLIT]

        # The agent selects one of the possible actions and sets it as their current status.
        self._statuses[hand] = random.choice(actions)

        if self._statuses[hand] == Enums.AgentStates.DOUBLE_DOWN:
            self._bet *= 2  # Double the bet
            self._chips -= self._bet  # Update the chips

        return self._statuses[hand]
