class Dealer:
    def __init__(self):
        self._status = "ACTIVE"
        self._cards = list()
        self._chips = 100000000
        self._bet = 0

    def is_agent_done(self):
        return self._status == "STAND" or self._status == "BUST"

    def get_agent_status(self):
        return self._status
    
    def get_name(self):
        return "John Ferguson"

    def get_chips(self):
        return self._chips
    
    def add_card_to_hand(self, card):
        self._cards.append(card)

    def get_hidden_hand(self):
        if len(self._cards) == 0:
            return []
        elif len(self._cards) == 1:
            return [self._cards[0], "?"]
        else:
            return [self._cards[0]] + ["?"] * (len(self._cards) - 1)
            
    def get_raw_hand(self):
        return self._cards

    def run_agent(self, is_debug):
        if is_debug:
            input("Press enter to continue\n")

        # if hand is less than 16, hit
        # if hand is greater than 17, stand
        self._status = "STAND"
