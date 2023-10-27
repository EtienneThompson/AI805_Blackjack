import random
from BaseAgent import BaseAgent
import Enums


class GavenAgent(BaseAgent):
    def run_agent(self, hand):
        self.wait_for_user_input()

        actions = [Enums.AgentStates.HIT, Enums.AgentStates.STAND]
        if self._bet * 2 <= self._chips:  # Check if the agent has enough chips to double down
            actions.append(Enums.AgentStates.DOUBLE_DOWN)
        if self.can_split(hand):
            actions.append(Enums.AgentStates.SPLIT)

        self._statuses[hand] = random.choice(actions)

        if self._statuses[hand] == Enums.AgentStates.DOUBLE_DOWN:
            self._bet *= 2  # Double the bet
            self._chips -= self._bet  # Update the chips

        return self._statuses[hand]
