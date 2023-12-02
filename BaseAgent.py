import random 
import Enums
import card_methods
from collections import defaultdict

class BaseAgent:
    def __init__(self, name, is_debug):
        self._name = name
        self._statuses = [Enums.AgentStates.ACTIVE]
        self._hands = list()
        self._hands.append(list())
        self._chips = 1000  # DO NOT CHANGE FROM 1000 CHIPS
        self._bets = list()
        self._is_split = False

        self._debug = is_debug

    def place_bet(self):
        """Base method for placing bets. Individual agents should override this method."""
        self._bets.append(min(self._chips, 50))
    
    def earn_chips(self, won_chips):
        self._chips += won_chips

    def get_name(self):
        if self._is_split:
            return self._name + " SPLIT"
        return self._name

    def get_agent_status(self, hand=0):
        agentState = str(self._statuses[hand])
        return agentState.split(".")[1]

    def does_agent_have_split_hand(self):
        return self._is_split

    def get_number_of_hands(self):
        return len(self._hands)

    def get_hand(self, hand=0):
        return self._hands[hand]

    def get_chips(self):
        return self._chips

    def get_bet(self, hand=0):
        if len(self._bets) <= hand:
            return 0
        return self._bets[hand]

    def is_agent_done(self):
        for status in self._statuses:
            if (status != Enums.AgentStates.STAND and
                    status != Enums.AgentStates.BUST and
                    status != Enums.AgentStates.DOUBLE_DOWN):
                return False

        return True

    def is_agent_hand_done(self, hand):
        return (self._statuses[hand] == Enums.AgentStates.STAND or
                self._statuses[hand] == Enums.AgentStates.BUST or
                self._statuses[hand] == Enums.AgentStates.DOUBLE_DOWN)

    def add_card_to_hand(self, card, hand=0):
        self._hands[hand].append(card)

    def set_status(self, new_status, hand=0):
        self._statuses[hand] = new_status

    def can_split(self, hand=0):
        if len(self._hands[hand]) == 2 and self._hands[hand][0][:-1] == self._hands[hand][1][:-1]:
            return True
        return False

    def split_hand(self, new_card_1, new_card_2):
        self._hands.append(list())
        self._statuses.append(Enums.AgentStates.ACTIVE)
        self._is_split = True
        for index in range(0, len(self._hands)):
            if self.can_split(index):
                new_hand_index = len(self._hands) - 1
                self._hands[new_hand_index].append(self._hands[index].pop())
                self._hands[index].append(new_card_1)
                self._hands[new_hand_index].append(new_card_2)
                self._bets.append(self._bets[index])
                self._chips -= self._bets[index]
                break

    def reset_after_round(self):
        self._hands = list()
        self._hands.append(list())
        self._statuses = [Enums.AgentStates.ACTIVE]
        self._bets = list()
        self._is_split = False

    def debug(self, data):
        if self._debug:
            print(data)

    def wait_for_user_input(self):
        if self._debug:
            command = input(
                "Press any key to continue, or \"exit\" to finish\n")

            if command == "exit":
                exit(0)
