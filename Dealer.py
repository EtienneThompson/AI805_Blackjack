from BaseAgent import BaseAgent
import Enums
import card_methods


class Dealer(BaseAgent):
    def get_hidden_hand(self):
        if len(self._cards) == 0: # Check if the dealer has empty cards 
            return []  # If the dealer has no cards, return an empty list 
        elif len(self._cards) == 1:  # This checks if the dealer has only one card 
            # If the dealer has one card, it's shown to the players so it's returned as it is
            # The second card, which the dealer hasn't received yet, is represented by a question mark ("?")
            return [self._cards[0], "?"] 
        else: # This part covers situation where dealer has more than one card 
            # [self._cards[0]] this part takes the first card of the dealer(that's shown to the players)
            # ["?"] * (len(self._cards) - 1) This part creates a list of question marks ("?"). 
            # The number of question marks equals the number of the dealer's card minus one. 
            # This represents all the dealer's cards other than the first one, which remain hidden from the players. 
            return [self._cards[0]] + ["?"] * (len(self._cards) - 1)

    def get_raw_hand(self): # This part reveals all the dealer's cards. 
        return self._cards

    def run_agent(self):
        self.wait_for_user_input() # This is waiting user input like 'enter' or 'exit'
        
        while True:
            # This part calculates the total value of the dealer's had using a method from the card_methods. 
            hand_value = card_methods.calculate_hand_value(self._cards) 
            if hand_value < 17: # If the dealer's had value is less than 17, they must take another card.
                self._status = Enums.AgentStates.HIT # This part sets dealer's action status to 'HIT'
            # This part checks for the special scenario called "soft 17" which occurs when the dealer has an Ace(which can 
            # count as 1 or 11) and a 6. If the dealer has soft 17, then the dealer needs to hit.      
            elif hand_value == 17 and "A" in self._cards and len(self._cards) == 2:
                # This condition checks for "soft 17" (i.e., Ace and 6)
                self._status = Enums.AgentStates.HIT # sets dealer's action status to 'HIT' 
            else: # When none of the above conditions are true. This would be when dealer's hand value is either 17 without an Ace and 6(not soft 17), 
                  # or it's 18 or higher. 
                self._status = Enums.AgentStates.STAND # set dealer's action status to 'STAND' meaning they will not take anymore cards.
                break # dealer breaks out ot make final decision. 

        return self._status # dealer's final action status 'HIT' or 'STAND' is returned. 
