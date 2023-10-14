import random

class Agent3:
    def __init__(self, name):
        self._name = name
        self._status = "ACTIVE"
        self._cards = list()
        self._chips = 1000  # DO NOT CHANGE FROM 1000 CHIPS
        self._bet = 0

    def get_name(self):
        return self._name

    def get_agent_status(self):
        return self._status

    def get_hand(self):
        return self._cards

    def get_chips(self):
        return self._chips

    def get_bet(self):
        return self._bet

    def is_agent_done(self):
        return self._status == "STAND" or self._status == "BUST" or self._status == "DOUBLE DOWN"

    def add_card_to_hand(self, card):
        self._cards.append(card)

    def can_split(self):
        if len(self._cards) == 2 and self._cards[0] == self._cards[1]:
            return True
        return False

    def run_agent(self, is_debug):
        if is_debug:
            input("Press enter to continue\n")

        actions = ["HIT", "STAND"]
        if self._bet * 2 <= self._chips:  # Check if the agent has enough chips to double down
            actions.append("DOUBLE DOWN")
        if self.can_split():
            actions.append("SPLIT")

        self._status = random.choice(actions)

        if self._status == "DOUBLE DOWN":
            self._bet *= 2  # Double the bet
            self._chips -= self._bet  # Update the chips

        elif self._status == "SPLIT":
            # Logic for splitting the cards into two hands
            pass  # Implement this part as per your game logic
            
        return self._status
