import random # for the Q-learning greedy policy
from BaseAgent import BaseAgent
import Enums
import card_methods
from collections import defaultdict # for the Q-Learning. 
import pandas as pd # for statistics data colletion. 

class KevinAgent(BaseAgent):
    DEFAULT_BET = 50  # This will be the default betting amount
    EPSILON_DECAY = 0.99  # Decay factor for exploration rate. To reduce agent's exploration rate
    MIN_EPSILON = 0.1  # Minimum exploration rate. Minimum value that epsilon can decrease to. 
    
    ######### Initialize Q-Table #############  
    def __init__(self,name, is_debug):
        super().__init__(name,is_debug)
        # existing initialization code
        # missing key will have default value of 0.0. This is to avoid KeyError when accessing a qdict with a key that don't exist
        self.q_table = defaultdict(lambda: defaultdict(float)) #Initialize Q-table 
        self.alpha = 0.1 # learning rate
        self.gamma = 0.9 # discount factor  
        self.epsilon = 1.0
        self.display_q_table = True 
        self.game_statistics =[]
    
    ######### Set Policy #####################  
    def epsilon_greedy_policy(self, state, hand):
        if random.random() < self.epsilon: #The vaule of epsilon is between 0 and 1.
            # Need to put SPLIT as choice based if only can split 
            choices = [Enums.AgentStates.HIT, Enums.AgentStates.STAND, Enums.AgentStates.DOUBLE_DOWN, Enums.AgentStates.SPLIT]
            if self.can_split(hand): # Check if true for split 
               choices.append(Enums.AgentStates.SPLIT) # Then return SPLIT for agent state 
            return random.choice(choices)
        else: #in this case the agent will try to exploit what it has learned so far
            # Return the action with the highest Q-Value for the current state
            choices = [Enums.AgentStates.HIT, Enums.AgentStates.STAND, Enums.AgentStates.DOUBLE_DOWN, Enums.AgentStates.SPLIT]
            if self.q_table[state]:
                # Return the action with the highest Q-value for the current state
                return max(self.q_table[state], key=self.q_table[state].get)
            else:
                # If no actions are recorded for this state in the Q-table choose randomly 
                choices = [Enums.AgentStates.HIT, Enums.AgentStates.STAND, Enums.AgentStates.DOUBLE_DOWN, Enums.AgentStates.SPLIT]
                if self.can_split(hand):
                    choices.append(Enums.AgentStates.SPLIT)
                    return random.choice(choices)
    
    ######### Learning algorithm #############
    def learn(self, state, action, reward, next_state):
        old_value = self.q_table[state][action] # takes current Q-value from the Q-table for the given 'state' and 'action' 
        next_max = max(self.q_table[next_state].values()) # maximum Q-value for the next state(best possible future reward)
        
        # Q-Learning formula
        # new Q-value is the weighted sum of the old value and the learned value. 
        # The learned value is immediate reward plus the discounted maximum future reward. 
        # This part calculates the learning rate. 
        # This is also the part of Bellmen Equation in the Q-Learning 
        # Q(s,a) = (1-α) x Q(s,a) + α x (r x γ*max*Q(s',a'))
        
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        # Discount factor which determines importance of future rewards. 
        self.q_table[state][action] = new_value
        
        if self.display_q_table:
            self.print_q_table()
    
    def print_q_table(self): # check if Q-Table empty or not 
        print("\nCurrent Q-table:") # print if Q-Table not empty 
        for state, action in self.q_table.items(): # loop through Q-table which are key, value pairs. States are printed in consistent order.
            print(f"State {state}:") # Prints current situation the agent is in. 
            for action, value in action.items(): # loop over the items in the actions dictionary
                print(f"  Action {action}: {value:.2f}") # prints action identifier and it's Q-value. 
            print()
    
    def get_current_state(self,hand):
        hand_value = card_methods.calculate_hand_value(self._hands[hand])
        has_ace = any(card[:-1] == "A" for card in self._hands[hand]) # Indicate whether the hand is a "soft hand" which means having an Ace that can be considered as 11. 
        return (hand_value, has_ace)
    
    #This is the reward handling part 
    def get_reward(self, outcome):
        if outcome == "win":
            return 1
        elif outcome == "lose":
            return -1 
        else: # For draw or anything else. 
            return 0 
    
    def update_after_action(self, action, outcome, next_state, hand): # This is where Q-Table data being fed from blackjack class 
        reward = self.get_reward(outcome)
        current_state = self.get_current_state(hand) 
        self.learn(current_state, action, reward, next_state)

    def place_bet_by_hand(self, hand):  # this is new betting function
        """Decide how much to bet based on the current hand."""
        # Check if the hand contains an Ace or a 10-value card
        if "A" in self._hands[hand] or any(card[:-1] in ["10", "J", "Q", "K"] for card in self._hands[hand]):
            # Bet double the default amount, but not more than available chips
            return min(self._chips, self.DEFAULT_BET * 2)
        else:
            # Bet the default amount, but not more than available chips
            return min(self._chips, self.DEFAULT_BET)
            self._bets[hand] = 0

    def run_agent(self, hand):
        self.wait_for_user_input()

        # At the start of the round the Agent decides how much to bet.
        self._bet = self.place_bet_by_hand(hand)
        self._chips -= self._bet  # The agent deducts the bet amount from their total chips
        
        current_state = self.get_current_state(hand)
        action = self.epsilon_greedy_policy(current_state,hand)
        self._statuses[hand] = action

        if self._statuses[hand] == Enums.AgentStates.DOUBLE_DOWN:
            self._bet *= 2  # Double the bet
            self._chips -= self._bet  # Update the chips

        return self._statuses[hand]
    
    def update_statistics(self, outcome, final_chip_count): # passing in the outcome and final chip count after every end of game.
        self.game_statistics.append({
            "Game Outcome" : outcome,
            "Final Chip Count" : final_chip_count,
        })

    def export_to_excel(agent, filename="C:\BlackjackStatistics\blackjack_statistics.xlsx"): # export the result to excel file using openpyxl(Excel Writer tool on pandas library)
        df = pd.DataFrame(agent.game_statistics)
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='KevinAgent Statistics')