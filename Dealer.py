from BaseAgent import BaseAgent
import Enums
import card_methods


class Dealer(BaseAgent):
    def get_hidden_hand(self):
        if len(self._cards) == 0:
            return []
        elif len(self._cards) == 1:
            return [self._cards[0], "?"]
        else:
            return [self._cards[0]] + ["?"] * (len(self._cards) - 1)

    def get_raw_hand(self):
        return self._cards

    def run_agent(self):
        self.wait_for_user_input()

        if (card_methods.calculate_hand_value(self._cards) < 17):
            self._status = Enums.AgentStates.HIT
        else:
            self._status = Enums.AgentStates.STAND

        return self._status
