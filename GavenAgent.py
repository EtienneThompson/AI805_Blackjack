import random
from BaseAgent import BaseAgent
import Enums
import card_methods

def generate_random_genome():
    actions = ["HIT", "STAND", "DOUBLE_DOWN", "SPLIT"]
    hand_values = range(4, 22)  # 4 to 21 inclusive

    genome = {}
    for value in hand_values:
        action_probabilities = {action: random.random() for action in actions}
        total = sum(action_probabilities.values())
        normalized_probabilities = {action: prob / total for action, prob in action_probabilities.items()}
        genome[value] = normalized_probabilities

    return genome

class GavenAgent(BaseAgent):

    def __init__(self, genome, name, is_debug):
        # print(f"Initializing GavenAgent with genome: {genome}, name: {name}, is_debug: {is_debug}")
        super().__init__(name, is_debug)
        self.genome = genome

    def run_agent(self, hand):
        self.wait_for_user_input()
        hand_value = card_methods.calculate_hand_value(self._hands[hand])
        hand_value_str = str(hand_value)  # Convert to string to match JSON keys

        # Log the current hand value and the available strategies in the genome
        # print(f"[DEBUG] {self.get_name()} - Running agent for hand value: {hand_value_str}")
        # print(f"[DEBUG] Available strategies in genome: {self.genome.keys()}")

        if hand_value_str not in self.genome:
            # print(f"[WARNING] Missing strategy for hand value: {hand_value_str} in genome for {self.get_name()}")
            # Implement a default strategy or handle the missing key
            chosen_action = "STAND"  # Default action if strategy is missing
        else:
            action_probabilities = self.genome[hand_value_str]
            chosen_action = self.choose_action(action_probabilities)

            if chosen_action == "DOUBLE_DOWN":
                if self._chips >= self._bets[hand]:  # Ensure enough chips are available
                    self._chips -= self._bets[hand]  # Deduct additional bet amount
                    self._bets[hand] *= 2  # Double the bet
                else:
                    # print(f"[WARNING] Not enough chips for {self.get_name()} to double down. Adjusting probabilities and trying again.")
                    action_probabilities["DOUBLE_DOWN"] = 0
                    self.normalize_probabilities(action_probabilities)
                    chosen_action = self.choose_action(action_probabilities)

            # If chosen action is SPLIT and it's not allowed, choose another action
            while chosen_action == "SPLIT" and not self.can_split(hand):
                # print(f"[DEBUG] Hand {hand} cannot be split. Adjusting probabilities and trying again.")
                action_probabilities["SPLIT"] = 0
                self.normalize_probabilities(action_probabilities)
                chosen_action = self.choose_action(action_probabilities)

        # Convert chosen action to corresponding Enums.AgentStates
        action_enum = Enums.AgentStates[chosen_action]
        self._statuses[hand] = action_enum

        return action_enum

    
    def choose_action(self, action_probabilities):
        actions, probabilities = zip(*action_probabilities.items())
        total = sum(probabilities)
        r = random.uniform(0, total)
        upto = 0
        for action, probability in action_probabilities.items():
            if upto + probability >= r:
                # print(f"[DEBUG] Action: {action}, Probability: {probability}")
                return action
            upto += probability

    def normalize_probabilities(self, probabilities):
        total = sum(probabilities.values())
        if total == 0:
            # Avoid division by zero if all probabilities are zero
            return
        for action in probabilities:
            probabilities[action] /= total

    def earn_chips(self, amount):
        self._chips += amount