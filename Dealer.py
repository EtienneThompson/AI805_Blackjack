from BaseAgent import BaseAgent
import Enums
import card_methods

class Dealer(BaseAgent):
    def get_hidden_hand(self):
        # Return the first card and hide the rest
        return [self._hands[0][0]] + ["?"] * (len(self._hands[0]) - 1) if self._hands[0] else []

    def get_raw_hand(self):
        # Return the actual hand of the dealer
        return self._hands[0]

    def run_agent(self, _):
        self.wait_for_user_input()

        hand_value = card_methods.calculate_hand_value(self._hands[0])
        is_soft_17 = hand_value == 17 and "A" in self._hands[0] and len(self._hands[0]) == 2

        if hand_value < 17 or is_soft_17:
            self._status = Enums.AgentStates.HIT
        else:
            self._status = Enums.AgentStates.STAND

        return self._status
