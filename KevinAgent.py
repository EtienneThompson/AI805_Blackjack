import random
from BaseAgent import BaseAgent
import Enums
import card_methods


class KevinAgent(BaseAgent):
    DEFAULT_BET = 50  # This will be the default betting amount
    EPSILON_DECAY = 0.99  # Decay factor for exploration rate. To reduce agent's exploration rate
    MIN_EPSILON = 0.1  # Minimum exploration rate. Minimum value that epsilon can decrease to. 
    
    ######### Initialize Q-Table ############# 
    def __init__(self):
        super().__init__()
        # existing initialization code
        # missing key will have default value of 0.0. This is to avoid KeyError when accessing a qdict with a key that don't exist
        self.q_table = qdick(lambda: qdict(float))
        self.alpha = 0.1 # learning rate
        self.gamma = 0.9 # discount factor 
    
    ######### Set Policy #####################  
    def epsilon_greedy_policy(self, state, epsilon=0.1):
        if random.random() < epsilon: #The vaule of epsilon is between 0 and 1. 
            return random.choice([Enums.AgentStates.HIT, Enums.AgentStates.STAND, Enums.AgentStates.DOUBLE_DOWN, Enums.AgentStates.SPLIT])
        else: #in this case the agent will try to exploit what it has learned so far
            # Return the action with the highest Q-Value for the current state
            return max(self.q_table[state], key=self.q_table[state].get)
    
    ######### Learning algorithm #############
    def learn(self, state, action, reward, next_state):
        old_value = self.q_table[state][action] # takes current Q-value from the Q-table for the given 'state' and 'action' 
        next_max = max(self.q_table[next_state].values()) # maximum Q-value for the next state(best possible future reward)
        
        # Q-Learning formula
        # new Q-value is the weighted sum of the old value and the learned value. 
        # The learned value is immediate reward plus the discounted maximum future reward. 
        #This part calculates the learning rate. 
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        # Discount factor which determines importance of future rewards. 
        self.q_table[state][action] = new_value

    def place_bet(self, hand):  # this is new betting function
        """Decide how much to bet based on the current hand."""
        # Check if the hand contains an Ace or a 10-value card
        if "A" in self._hands[hand] or any(card[:-1] in ["10", "J", "Q", "K"] for card in self._hands[hand]):
            # Bet double the default amount, but not more than available chips
            return min(self._chips, self.DEFAULT_BET * 2)
        else:
            # Bet the default amount, but not more than available chips
            return min(self._chips, self.DEFAULT_BET)

    def run_agent(self, hand):
        self.wait_for_user_input()

        # At the start of the round the Agent decides how much to bet.
        self._bet = self.place_bet(hand)
        self._chips -= self._bet  # The agent deducts the bet amount from their total chips

        actions = [Enums.AgentStates.HIT, Enums.AgentStates.STAND]
        if self._bet * 2 <= self._chips:  # Check if the agent has enough chips to double down
            actions.append(Enums.AgentStates.DOUBLE_DOWN)
        if card_methods.can_split_hand(self._hands[hand]):
            actions.append(Enums.AgentStates.SPLIT)

        # The agent selects one of the possible actions and sets it as their current status.
        self._statuses[hand] = random.choice(actions)

        if self._statuses[hand] == Enums.AgentStates.DOUBLE_DOWN:
            self._bet *= 2  # Double the bet
            self._chips -= self._bet  # Update the chips

        return self._statuses[hand]
