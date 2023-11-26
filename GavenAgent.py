import random
from BaseAgent import BaseAgent
import Enums
import card_methods


class GavenAgent(BaseAgent):
    def run_agent(self, hand):
        self.wait_for_user_input()

        actions = [Enums.AgentStates.HIT, Enums.AgentStates.STAND]
        if self.get_bet(hand) * 2 <= self._chips:  # Check if the agent has enough chips to double down
            actions.append(Enums.AgentStates.DOUBLE_DOWN)
        if card_methods.can_split_hand(self._hands[hand]):
            actions.append(Enums.AgentStates.SPLIT)

        self._statuses[hand] = random.choice(actions)

        return self._statuses[hand]
