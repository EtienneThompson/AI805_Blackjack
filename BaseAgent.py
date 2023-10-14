import Enums


class BaseAgent:
    def __init__(self, name, is_debug):
        self._name = name
        self._status = Enums.AgentStates.ACTIVE
        self._cards = list()
        self._chips = 1000  # DO NOT CHANGE FROM 1000 CHIPS
        self._bet = 0

        self._debug = is_debug

    def get_name(self):
        return self._name

    def get_agent_status(self):
        agentState = str(self._status)
        return agentState.split(".")[1]

    def get_hand(self):
        return self._cards

    def get_chips(self):
        return self._chips

    def get_bet(self):
        return self._bet

    def is_agent_done(self):
        return (
            self._status == Enums.AgentStates.STAND or
            self._status == Enums.AgentStates.BUST or
            self._status == Enums.AgentStates.DOUBLE_DOWN)

    def add_card_to_hand(self, card):
        self._cards.append(card)

    def set_status(self, new_status):
        self._status = new_status

    def can_split(self):
        if len(self._cards) == 2 and self._cards[0] == self._cards[1]:
            return True
        return False

    def debug(self, data):
        if self._debug:
            print(data)

    def wait_for_user_input(self):
        if self._debug:
            command = input(
                "Press any key to continue, or \"exit\" to finish\n")

            if command == "exit":
                exit(0)
