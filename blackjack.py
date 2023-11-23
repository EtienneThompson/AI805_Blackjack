"""Runs a simulated game of blackjack."""
import random
from EtienneAgent import EtienneAgent
from GavenAgent import GavenAgent
from KevinAgent import KevinAgent
from Dealer import Dealer

import Enums
import card_methods

SUITS = ["♥", "♦", "♠", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
IS_DEBUG = False


def debug(data):
    """Prints to console only if the game is running in debug mode."""
    if IS_DEBUG:
        print(data)


def wait_for_user_input():
    """Waits for user input only if the game is running in debug mode."""
    if IS_DEBUG:
        command = input("Press any key to continue, or \"exit\" to finish\n")

        if command == "exit":
            exit(0)


def initialize_cards_randomly():
    """Generates card list and shuffles them around."""
    # Create eight decks
    cards = [rank + suit for suit in SUITS for rank in RANKS] * 8
    # Shuffle the combined eight decks
    random.shuffle(cards)
    return cards


def get_imperfection_parameters():
    """Randomly generate offsets used for shuffling."""
    split_offset = random.randint(-10, 10)  # Adjusted for more variability
    consecutive_drop = random.randint(1, 4)
    return split_offset, consecutive_drop


def shuffle_two_decks(cards, split_offset, consecutive_drop):
    """Shuffle roughly two decks from the given cards"""
    cards_to_shuffle = cards[:104]  # Two decks
    remaining_cards = cards[104:]
    shuffled = imperfect_riffle(
        cards_to_shuffle, split_offset, consecutive_drop)
    shuffled = strip_cut(shuffled)
    return shuffled + remaining_cards


def imperfect_riffle(cards, split_offset, consecutive_drop):
    """Perform a riffle shuffle on the deck of cards with imperfection"""
    middle = len(cards) // 2
    left = cards[:middle + split_offset]
    right = cards[middle + split_offset:]
    shuffled = []
    last_dropped = None  # Can be 'left' or 'right'
    consecutive_count = 0

    while left or right:
        if len(left) == 0:
            shuffled.append(right.pop(0))
            last_dropped = 'right'
        elif len(right) == 0:
            shuffled.append(left.pop(0))
            last_dropped = 'left'
        else:
            if last_dropped and consecutive_count < consecutive_drop:
                # Continuing the consecutive drop from the same half
                if last_dropped == 'left':
                    shuffled.append(left.pop(0))
                else:
                    shuffled.append(right.pop(0))
                consecutive_count += 1
            else:
                # Alternating the drop between halves
                if len(left) > len(right):
                    shuffled.append(left.pop(0))
                    last_dropped = 'left'
                else:
                    shuffled.append(right.pop(0))
                    last_dropped = 'right'
                consecutive_count = 1

    return shuffled


def strip_cut(cards):
    """Cut the deck of cards in two"""
    cut_length = 4
    segments = [cards[i:i+cut_length]
                for i in range(0, len(cards), cut_length)]
    return [card for segment in reversed(segments) for card in segment]


def shuffle_cards():
    """Shuffle the decks of cards together."""
    global CARDS
    split_offset, consecutive_drop = get_imperfection_parameters()
    for _ in range(4):  # Iterate this based on your desired level of shuffling
        CARDS = shuffle_two_decks(CARDS, split_offset, consecutive_drop)
        CARDS = shuffle_two_decks(
            CARDS[104:], split_offset, consecutive_drop) + CARDS[:104]
        CARDS = shuffle_two_decks(
            CARDS[208:], split_offset, consecutive_drop) + CARDS[:208]
        CARDS = shuffle_two_decks(
            CARDS[312:], split_offset, consecutive_drop) + CARDS[:312]


CARDS = initialize_cards_randomly()
shuffle_cards()


def deal_cards(dealer, player1, player2, player3, player4, player5, player6):
    """Deal cards to each of the players"""
    players_order = [player6, player5, player4, player3, player2, player1]
    for _ in range(2):
        for player in players_order:
            player.add_card_to_hand(CARDS.pop())
            print_table(dealer, player1, player2, player3,
                        player4, player5, player6, is_dealer_turn=False)
            wait_for_user_input()

        dealer.add_card_to_hand(CARDS.pop())
        print_table(dealer, player1, player2, player3,
                    player4, player5, player6, is_dealer_turn=False)
        wait_for_user_input()


def formatted_column(text, width):
    """Center the text within the specified width."""
    return text.center(width)


def formatted_dollar(amount):
    """Return amount formatted as dollar string with commas."""
    return "${:,.0f}".format(amount)


def formatted_cards(cards_list, width=None):
    """Format the card list into a clean string."""
    cards_str = ", ".join(cards_list)
    if width and not cards_str:  # If width is provided and cards_str is empty
        cards_str = ''  # Return empty string and let formatted_column handle the padding
    return cards_str


def calculate_max_widths(dealer, *agents):
    """Compute max widths for columns in the print table"""
    # For Name Column
    max_name_label = len(" PLAYERS ")  # Length of the label in the header
    max_name_content = max(
        [agent.get_name() for agent in agents] + ['Dealer', dealer.get_name()], key=len)
    max_name = max(max_name_label, len(max_name_content) + 2)

    # For Chips Column
    max_chips_label = len(" CHIPS ")
    max_chips_content = max([formatted_dollar(agent.get_chips(
    )) for agent in agents] + [formatted_dollar(dealer.get_chips())], key=len)
    max_chips = max(max_chips_label, len(max_chips_content) + 2)

    # For Cards Column
    max_hand_label = len(" CARDS ")
    max_hand_content = 0
    for agent in agents:
        # Need to determine max length of all hands
        for i in range(0, agent.get_number_of_hands()):
            max_size = max([formatted_cards(agent.get_hand(
                i))] + [formatted_cards(dealer.get_hidden_hand())], key=len)
            max_hand_content = max(len(max_size), max_hand_content)
    max_hand = max(max_hand_label, max_hand_content + 2)

    # For Bet Column
    max_bet_label = len(" BET ")
    max_bet_content = max([formatted_dollar(agent.get_bet())
                          for agent in agents] + ["$0"], key=len)
    max_bet = max(max_bet_label, len(max_bet_content) + 2)

    # For Status Column
    max_status_label = len(" STATUS ")
    max_status_content = 0
    for agent in agents:
        # Need to determine max length of all hands
        for i in range(0, agent.get_number_of_hands()):
            max_size = max([agent.get_agent_status(i)] +
                           ['ACTIVE', dealer.get_agent_status()], key=len)
            max_status_content = max(len(max_size), max_status_content)
    max_status = max(max_status_label, max_status_content + 2)

    # Return max lengths, +2 is for padding
    return max_name + 2, max_chips + 2, max_hand + 2, max_bet + 2, max_status + 2


def print_table(dealer, *agents, is_dealer_turn, q_table=None):
    """Print table data of each player and dealer"""
    max_name_width, max_chips_width, max_hand_width, max_bet_width, max_status_width = calculate_max_widths(
        dealer, *agents)

    # Separator
    sep_line = "*" * (max_name_width + max_chips_width + max_hand_width +
                      max_status_width + max_bet_width + 14)  # 14 is for the "|" separators and spaces
    debug(sep_line)

    dealer_cards = dealer.get_hidden_hand()
    if is_dealer_turn:
        dealer_cards = dealer.get_raw_hand()
    # Print Dealer's details
    debug("|" + formatted_column(" DEALER ", max_name_width) + "|" + formatted_column(" CHIPS ", max_chips_width) +
          "|" + formatted_column(" CARDS ", max_hand_width) + "|" + formatted_column(" STATUS ", max_status_width) + "|")
    debug("|" + formatted_column(" " + dealer.get_name() + " ", max_name_width) + "|" + formatted_column(" " + formatted_dollar(dealer.get_chips()) + " ", max_chips_width) + "|" +
          formatted_column(" " + formatted_cards(dealer_cards, max_hand_width) + " ", max_hand_width) + "|" + formatted_column(" " + dealer.get_agent_status() + " ", max_status_width) + "|")

    debug(sep_line)

    # Print table header for agents
    debug("|" + formatted_column(" PLAYERS ", max_name_width) + "|" + formatted_column(" CHIPS ", max_chips_width) + "|" + formatted_column(
        " CARDS ", max_hand_width) + "|" + formatted_column(" BET ", max_bet_width) + "|" + formatted_column(" STATUS ", max_status_width) + "|")

    # Print Agent details
    for agent in agents:
        for i in range(0, agent.get_number_of_hands()):
            debug("|" + formatted_column(" " + agent.get_name() + " ", max_name_width) + "|" + formatted_column(" " + formatted_dollar(agent.get_chips()) + " ", max_chips_width) + "|" + formatted_column(" " + formatted_cards(agent.get_hand(i),
                  max_hand_width) + " ", max_hand_width) + "|" + formatted_column(" " + formatted_dollar(agent.get_bet()) + " ", max_bet_width) + "|" + formatted_column(" " + agent.get_agent_status(i) + " ", max_status_width) + "|")

    debug(sep_line)
    
    if q_table is not None: # check if Q-Table empty or not 
        print("\nQ-table for KevinAgent:") # print if Q-Table not empty 
        for state, actions in sorted(q_table.items()): # loop through Q-table which are key, value pairs. States are printed in consistent order. 
            print(f"State {state}:")  # Prints current situation the agent is in. 
            for action, value in sorted(actions.items()): # loop over the items in the actions dictionary
                print(f"   Action {action}: {value: .2f}") # prints action identifier and it's Q-value. 
        print()        

def handle_agent_choice(choice, agent, hand):
    """Handle agent's choice"""
    if choice == Enums.AgentStates.HIT:
        new_card = CARDS.pop()
        agent.add_card_to_hand(new_card, hand)
        # Update the agent's status if needed
        # (You'll need to implement the `calculate_hand_value` function)
        if card_methods.calculate_hand_value(agent.get_hand()) > 21:
            agent.set_status(Enums.AgentStates.BUST, hand)
    elif choice == Enums.AgentStates.STAND:
        agent.set_status(Enums.AgentStates.STAND, hand)
    elif choice == Enums.AgentStates.DOUBLE_DOWN:
        new_card = CARDS.pop()
        agent.add_card_to_hand(new_card, hand)
        agent._bet *= 2  # Double the bet
        agent._chips -= agent._bet  # Update the chips
    elif choice == Enums.AgentStates.SPLIT:
        new_card_1 = CARDS.pop()
        new_card_2 = CARDS.pop()
        agent.split_hand(new_card_1, new_card_2)


def run_turn_for_agent(agent, dealer, all_players):
    """Let agent make choices until in finished state"""
    debug(f"{agent.get_name()}'s turn is running")
    while not agent.is_agent_done():
        # Run a single move for each hand that is available.
        for i in range(0, agent.get_number_of_hands()):
            if agent.is_agent_hand_done(i):
                continue  # skip any already finished hands.

            print_table(dealer, *all_players, is_dealer_turn=(agent == dealer))

            choice = agent.run_agent(i)
            handle_agent_choice(choice, agent, i)


def run_full_game():
    """Run each player's turn and the dealer"""
    debug("Starting a new game")
    dealer = Dealer("Dealer", IS_DEBUG)
    players = [
        EtienneAgent("Etienne Agent 1", IS_DEBUG),
        GavenAgent("Gaven Agent 1", IS_DEBUG),
        KevinAgent("Kevin Agent 1", IS_DEBUG),
        EtienneAgent("Etienne Agent 2", IS_DEBUG),
        GavenAgent("Gaven Agent 2", IS_DEBUG),
        KevinAgent("Kevin Agent 2", IS_DEBUG)
    ]

    debug("Initializing deck of cards")
    global CARDS
    CARDS = initialize_cards_randomly()

    debug("Shuffling deck of cards")
    shuffle_cards()

    debug("Dealing out initial cards")
    deal_cards(dealer, *players)

    for player in players:
        run_turn_for_agent(player, dealer, players)
        if isinstance(player, KevinAgent):
            # Update epsilon for exploration/exploitation balance
            player.epsilon = max(player.MIN_EPSILON, player.epsilon * player.EPSILON_DECAY)
            player.print_q_table() # prints Q-table

    run_turn_for_agent(dealer, dealer, players) # Point where to feed Q-learning. 
    
    for player in players:
        if isinstance(player, KevinAgent): # Loop through each player and make sure it gets applied to KevinAgent only 
            for i in range(player.get_number_of_hands()): # iterate over each hand of KevinAgent 
                next_state = player.get_current_state(i)  # determine next state
                if card_methods.calculate_hand_value(player.get_hand(i)) > 21: # If the player hand value exceed 21 (bust)
                    outcome = "lose"
                elif card_methods.calculate_hand_value(dealer.get_hand()) > 21: # Dealer hand value exceed 21 (dealer bust) 
                    outcome = "win"
                elif card_methods.calculate_hand_value(player.get_hand(i)) > card_methods.calculate_hand_value(dealer.get_hand()): # Player hand greater than dealer
                    outcome = "win"
                elif card_methods.calculate_hand_value(player.get_hand(i)) < card_methods.calculate_hand_value(dealer.get_hand()): # Player hand less than dealer 
                    outcome = "lose"
                else:
                    outcome = "draw" # player and dealer hand vaule equal 
                player.update_after_action(player._statuses[i], outcome, next_state, i) # Updates Q-Table on KevinAgent 

    print_table(dealer, *players, is_dealer_turn=True)

    debug("Ending game")


def main():
    requested_exit = False
    simulation_iterations = 0
    max_simulation_iterations = 1000

    print("Do you want to run in debug or simulation mode?")
    mode = input("Type 1 for debug, 2 for simulation\n")

    global IS_DEBUG
    if mode == "1":
        IS_DEBUG = True
    elif mode == "2":
        IS_DEBUG = False
    else:
        print("Your input of " + mode +
              " is not a valid option. Please try again with a valid mode.")
        exit(1)

    while not requested_exit:
        run_full_game()

        simulation_iterations += 1
        print("Completed " + str(simulation_iterations) + " out of " +
              str(max_simulation_iterations) + " iterations.")
        print(str(100 * (simulation_iterations /
              max_simulation_iterations)) + "% Complete")

        wait_for_user_input()

        if simulation_iterations == max_simulation_iterations:
            requested_exit = True


if __name__ == "__main__":
    main()
