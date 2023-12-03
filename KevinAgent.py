import random # for the Q-learning greedy policy
from BaseAgent import BaseAgent
import Enums
import card_methods
from collections import defaultdict # for the Q-Learning. 
import pandas as pd # for statistics data colletion. 
import os # file handling

class KevinAgent(BaseAgent):
    DEFAULT_BET = 50  # This will be the default betting amount
    EPSILON_DECAY = 0.995  # Decay factor for exploration rate. To reduce agent's exploration rate. Set from 0.99 to 0.995 for more gradual decay. 
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
        self.last_action = None # last action default value 
        self.last_q_value = 0 # Initialize the last Q-value 
    
    ######### Set Policy #####################  
    def epsilon_greedy_policy(self, state, hand):
        valid_actions = [Enums.AgentStates.HIT, Enums.AgentStates.STAND]
        # first check for SPLIT and DOUBLE_DOWN situation 
        if self.can_split(hand):
            valid_actions.append(Enums.AgentStates.SPLIT)
        if len(self._hands[hand]) == 2:  # Check for initial hand for DOUBLE_DOWN
            valid_actions.append(Enums.AgentStates.DOUBLE_DOWN)

        if random.random() < self.epsilon: #The vaule of epsilon is between 0 and 1.
            return random.choice(valid_actions)
        else:
            if self.q_table[state]:
                return max(self.q_table[state], key=self.q_table[state].get) # Return the action with the highest Q-value for the current state
            else:
                return random.choice(valid_actions) # If no actions are recorded for this state in the Q-table choose randomly
    
    ######### Learning algorithm #############
    def learn(self, state, action, reward, next_state):
        old_value = self.q_table[state][action] # takes current Q-value from the Q-table for the given 'state' and 'action' 
        next_max = max(self.q_table[next_state].values(), default=0) # maximum Q-value for the next state(best possible future reward). Use default if no next state. 
        
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

    def place_bet_by_hand(self, hand):  # this is new betting function
        """Decide how much to bet based on the current hand."""
        # Check if the hand contains an Ace or a 10-value card
        if "A" in self._hands[hand] or any(card[:-1] in ["10", "J", "Q", "K"] for card in self._hands[hand]):
            # Bet double the default amount, but not more than available chips
            return min(self._chips, self.DEFAULT_BET * 2)
        else:
            # Bet the default amount, but not more than available chips
            self._bets[hand] = 0
            return min(self._chips, self.DEFAULT_BET)
            
    def run_agent(self, hand):
        self.wait_for_user_input()
        
        # Check if the hand index is within the valid range ######## Deal with Index out of range Error 
        if hand < 0 or hand >= len(self._hands):
            raise IndexError(f"Hand index {hand} out of range for agent {self.get_name()}")
        
        current_state = self.get_current_state(hand)
        action = self.epsilon_greedy_policy(current_state,hand)
        
        # Check if the state and action pair exists in the Q-table and retrieve the Q-value
        if current_state in self.q_table and action in self.q_table[current_state]:
            q_value = self.q_table[current_state][action]
        else:
            q_value = 0 # Use a default Q-value if the state-action pair is not in the Q-table
        
        self.last_q_value = q_value # Store the last Q-value
        
        # Ensure that status list is long enough to accomodate the hand index ###### Deal with index out of range error. 
        if hand >= len(self._statuses):
            # Extend the _statuses lis with default values (None or Enum.AgentStates.ACTIVE)
            self._statuses.extend([None] * (hand - len(self._statuses) + 1))
        
        self._statuses[hand] = action
        
        action_str = str(action)
        if '.' in action_str:
            self.last_action = action_str.split('.')[1] # Split action result text and only take out the second one. 
        else:
            self.last_action = action_str
        
        ########## Update epsilon with Decay #############
        self.epsilon = max(self.MIN_EPSILON, self.epsilon * self.EPSILON_DECAY) # Ensure decay is applied after each action 
        
        return action 
    
    ######## Deal with Index Out of Range Error ###########
    def get_status(self, hand):
    # Ensure that the hand index is within the range before accessing it
        if hand < 0 or hand >= len(self._statuses):
            raise IndexError(f"Status index {hand} out of range for agent {self.get_name()}")
        return str(self._statuses[hand]).split(".")[1] if self._statuses[hand] is not None else 'UNKNOWN'
    ######## Deal with Index Out of Range Error ###########
    
    def update_after_action(self, action, outcome, next_state, hand): # This is where Q-Table data being fed from blackjack class 
        reward = self.get_reward(outcome)
        current_state = self.get_current_state(hand)
        
        # This is additional check for end of state. 
        if outcome in ("win", "lose", "draw"):
            next_state = None # Indicate end of game. 
         
        self.learn(current_state, action, reward, next_state)
    
    def update_statistics(self, outcome, final_chip_count, last_actions, last_q_value): # passing in the outcome, final chip count, last action from Q-value and the Q-value itself after every end of game.
        outcome_value = 1 if outcome == "win" else 0 # Change win to 1 and lose and draw to 0 for better statistical anlaysis. 
        self.game_statistics.append({
            "Game Outcome" : outcome_value,
            "Final Chip Count" : final_chip_count,
            "Action from Q-value" : last_actions,
            "Q-value" : last_q_value 
        })

    def export_to_excel(self, filename="C:\\BlackjackStatistics\\blackjack_statistics.xlsx"):
        df = pd.DataFrame(self.game_statistics)
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='KevinAgent Statistics')