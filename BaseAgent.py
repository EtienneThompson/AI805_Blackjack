import random 
import Enums
import card_methods
from collections import defaultdict

class BaseAgent:
    INITIAL_CHIPS = 1000  # Class constant for initial chip amount

    def __init__(self, name: str, is_debug: bool):
        self._name = name
        self._statuses = [Enums.AgentStates.ACTIVE]
        self._hands = [[]]
        self._chips = BaseAgent.INITIAL_CHIPS
        self._bets = []
        self._is_split = False
        self._debug = is_debug

    def place_bet(self):
        """Places a bet. To be overridden in derived classes."""
        self._bets.append(min(self._chips, 50))
    
    def earn_chips(self, won_chips: int):
        """Adds the specified amount of chips to the agent's total."""
        self._chips += won_chips

    def get_name(self) -> str:
        """Returns the agent's name. Appends 'SPLIT' if the agent has a split hand."""
        return f"{self._name} SPLIT" if self._is_split else self._name

    def get_status(self, hand: int = 0) -> str:
        """Returns the status of the agent for a specific hand."""
        return str(self._statuses[hand]).split(".")[1]

    def does_agent_have_split_hand(self) -> bool:
        """Checks if the agent has a split hand."""
        return self._is_split

    def get_number_of_hands(self) -> int:
        """Returns the number of hands the agent has."""
        return len(self._hands)

    def get_hand(self, hand: int = 0) -> list:
        """Returns a specific hand of the agent."""
        return self._hands[hand]

    def get_chips(self) -> int:
        """Returns the total number of chips the agent has."""
        return self._chips

    def get_bet(self, hand: int = 0) -> int:
        """Returns the bet amount for a specific hand."""
        return self._bets[hand] if len(self._bets) > hand else 0

    def is_agent_done(self) -> bool:
        """Checks if the agent is done with all hands."""
        print(f"Current statuses: {self._statuses}")
        return all(status in {Enums.AgentStates.STAND, Enums.AgentStates.BUST, Enums.AgentStates.DOUBLE_DOWN} 
                   for status in self._statuses)

    def is_agent_hand_done(self, hand: int) -> bool:
        """Checks if a specific hand of the agent is done."""
        status = self._statuses[hand]
        return status in {Enums.AgentStates.STAND, Enums.AgentStates.BUST, Enums.AgentStates.DOUBLE_DOWN}

    def add_card_to_hand(self, card, hand: int = 0):
        """Adds a card to a specific hand of the agent."""
        self._hands[hand].append(card)

    def set_status(self, new_status, hand: int = 0):
        """Sets the status of a specific hand of the agent."""
        print(f"Setting status of hand {hand} to {new_status}")
        self._statuses[hand] = new_status

    def can_split(self, hand: int = 0) -> bool:
        """Checks if the agent can split a specific hand."""
        hand_cards = self._hands[hand]
        return len(hand_cards) == 2 and hand_cards[0][:-1] == hand_cards[1][:-1]

    def split_hand(self, new_card_1, new_card_2):
        """Splits the agent's hand, creating a new hand and updating bets and chips."""
        self._hands.append([])
        self._statuses.append(Enums.AgentStates.ACTIVE)
        self._is_split = True

        for index, hand_cards in enumerate(self._hands[:-1]):
            if self.can_split(index):
                self._hands[-1].append(hand_cards.pop())
                hand_cards.append(new_card_1)
                self._hands[-1].append(new_card_2)
                self._bets.append(self._bets[index])
                self._chips -= self._bets[index]
                break

    def reset_after_round(self):
        """Resets the agent's state after a round."""
        self._hands = [[]]
        self._statuses = [Enums.AgentStates.ACTIVE]
        self._bets = []
        self._is_split = False

    def debug(self, data: str):
        """Prints debug information if debug mode is enabled."""
        if self._debug:
            print(data)

    def wait_for_user_input(self):
        """Waits for user input in debug mode. Exits if 'exit' is input."""
        if self._debug:
            command = input("Press any key to continue, or 'exit' to finish\n")
            if command == "exit":
                exit(0)
