import Enums


class BaseAgent:
    def __init__(self, name, is_debug):
        self._name = name
        self._status = Enums.AgentStates.ACTIVE
        self._hands = list()
        self._hands.append(list())
        self._chips = 1000  # DO NOT CHANGE FROM 1000 CHIPS
        self._bet = 0
        self._is_split = False

        self._debug = is_debug

    def get_name(self):
        if self._is_split:
            return self._name + " SPLIT"
        return self._name

    def get_agent_status(self):
        agentState = str(self._status)
        return agentState.split(".")[1]

    def does_agent_have_split_hand(self):
        return self._is_split

    def get_number_of_hands(self):
        return len(self._hands)

    def get_hand(self, hand=0):
        return self._hands[hand]

    def get_chips(self):
        return self._chips

    def get_bet(self):
        return self._bet

    def is_agent_done(self):
        return (
            self._status == Enums.AgentStates.STAND or
            self._status == Enums.AgentStates.BUST or
            self._status == Enums.AgentStates.DOUBLE_DOWN)

    def add_card_to_hand(self, card, hand=0):
        self._hands[hand].append(card)

    def set_status(self, new_status):
        self._status = new_status

    def can_split(self, hand=0):
        if len(self._hands[hand]) == 2 and self._hands[hand][0][:-1] == self._hands[hand][1][:-1]:
            return True
        return False

    def split_hand(self, new_card_1, new_card_2):
        self._hands.append(list())
        self._is_split = True
        for index in range(0, len(self._hands)):
            if self.can_split(index):
                new_hand_index = len(self._hands) - 1
                self._hands[new_hand_index].append(self._hands[index].pop())
                self._hands[index].append(new_card_1)
                self._hands[new_hand_index].append(new_card_2)

    def debug(self, data):
        if self._debug:
            print(data)

    def wait_for_user_input(self):
        if self._debug:
            command = input(
                "Press any key to continue, or \"exit\" to finish\n")

            if command == "exit":
                exit(0)
