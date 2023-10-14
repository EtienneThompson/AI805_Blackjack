import random
from Agent1 import Agent1
from Agent2 import Agent2
from Agent3 import Agent3
from Dealer import Dealer

SUITS = ["♥", "♦", "♠", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def initialize_cards_randomly():
    # Create eight decks
    cards = [rank + suit for suit in SUITS for rank in RANKS] * 8  
    # Shuffle the combined eight decks
    random.shuffle(cards)
    return cards

def get_imperfection_parameters():
    split_offset = random.randint(-10, 10)  # Adjusted for more variability
    consecutive_drop = random.randint(1, 4)
    return split_offset, consecutive_drop

def shuffle_two_decks(cards, split_offset, consecutive_drop):
    """Shuffle roughly two decks from the given cards"""
    cards_to_shuffle = cards[:104]  # Two decks
    remaining_cards = cards[104:]
    shuffled = imperfect_riffle(cards_to_shuffle, split_offset, consecutive_drop)
    shuffled = strip_cut(shuffled)
    return shuffled + remaining_cards

def imperfect_riffle(cards, split_offset, consecutive_drop):
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
    cut_length = 4
    segments = [cards[i:i+cut_length] for i in range(0, len(cards), cut_length)]
    return [card for segment in reversed(segments) for card in segment]

def shuffle_cards():
    global CARDS
    split_offset, consecutive_drop = get_imperfection_parameters()
    for _ in range(4):  # Iterate this based on your desired level of shuffling
        CARDS = shuffle_two_decks(CARDS, split_offset, consecutive_drop)
        CARDS = shuffle_two_decks(CARDS[104:], split_offset, consecutive_drop) + CARDS[:104]
        CARDS = shuffle_two_decks(CARDS[208:], split_offset, consecutive_drop) + CARDS[:208]
        CARDS = shuffle_two_decks(CARDS[312:], split_offset, consecutive_drop) + CARDS[:312]

CARDS = initialize_cards_randomly()
shuffle_cards()

def deal_cards(dealer, player1, player2, player3, player4, player5, player6, is_debug):
    players_order = [player6, player5, player4, player3, player2, player1]
    for _ in range(2):
        for player in players_order:
            player.add_card_to_hand(CARDS.pop())
            if is_debug:
                print_table(dealer, player1, player2, player3, player4, player5, player6)
                input("Press any key to continue...")
        dealer.add_card_to_hand(CARDS.pop())
        if is_debug:
            print_table(dealer, player1, player2, player3, player4, player5, player6)
            input("Press any key to continue...")

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
    # For Name Column
    max_name_label = len(" PLAYERS ")  # Length of the label in the header
    max_name_content = max([agent.get_name() for agent in agents] + ['Dealer', dealer.get_name()], key=len)
    max_name = max(max_name_label, len(max_name_content) + 2)

    # For Chips Column
    max_chips_label = len(" CHIPS ")
    max_chips_content = max([formatted_dollar(agent.get_chips()) for agent in agents] + [formatted_dollar(dealer.get_chips())], key=len)
    max_chips = max(max_chips_label, len(max_chips_content) + 2)

    # For Cards Column
    max_hand_label = len(" CARDS ")
    max_hand_content = max([formatted_cards(agent.get_hand()) for agent in agents] + [formatted_cards(dealer.get_hidden_hand())], key=len)
    max_hand = max(max_hand_label, len(max_hand_content) + 2)

    # For Bet Column
    max_bet_label = len(" BET ")
    max_bet_content = max([formatted_dollar(agent.get_bet()) for agent in agents] + ["$0"], key=len)
    max_bet = max(max_bet_label, len(max_bet_content) + 2)

    # For Status Column
    max_status_label = len(" STATUS ")
    max_status_content = max([agent.get_agent_status() for agent in agents] + ['ACTIVE', dealer.get_agent_status()], key=len)
    max_status = max(max_status_label, len(max_status_content) + 2)

    # Return max lengths, +2 is for padding
    return max_name + 2, max_chips + 2, max_hand + 2, max_bet + 2, max_status + 2

def print_table(dealer, *agents):
    max_name_width, max_chips_width, max_hand_width, max_bet_width, max_status_width = calculate_max_widths(dealer, *agents)

    # Separator
    sep_line = "*" * (max_name_width + max_chips_width + max_hand_width + max_status_width + max_bet_width + 14)  # 14 is for the "|" separators and spaces
    print(sep_line)

    # Print Dealer's details
    print("|" + formatted_column(" DEALER ", max_name_width) + "|" + formatted_column(" CHIPS ", max_chips_width) + "|" + formatted_column(" CARDS ", max_hand_width) + "|" + formatted_column(" STATUS ", max_status_width) + "|")
    print("|" + formatted_column(" " + dealer.get_name() + " ", max_name_width) + "|" + formatted_column(" " + formatted_dollar(dealer.get_chips()) + " ", max_chips_width) + "|" + formatted_column(" " + formatted_cards(dealer.get_hidden_hand(), max_hand_width) + " ", max_hand_width) + "|" + formatted_column(" " + dealer.get_agent_status() + " ", max_status_width) + "|")

    print(sep_line)

    # Print table header for agents
    print("|" + formatted_column(" PLAYERS ", max_name_width) + "|" + formatted_column(" CHIPS ", max_chips_width) + "|" + formatted_column(" CARDS ", max_hand_width) + "|" + formatted_column(" BET ", max_bet_width) + "|" + formatted_column(" STATUS ", max_status_width) + "|")
    
    # Print Agent details
    for agent in agents:
        print("|" + formatted_column(" " + agent.get_name() + " ", max_name_width) + "|" + formatted_column(" " + formatted_dollar(agent.get_chips()) + " ", max_chips_width) + "|" + formatted_column(" " + formatted_cards(agent.get_hand(), max_hand_width) + " ", max_hand_width) + "|" + formatted_column(" " + formatted_dollar(agent.get_bet()) + " ", max_bet_width) + "|" + formatted_column(" " + agent.get_agent_status() + " ", max_status_width) + "|")

    print(sep_line)

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        card_rank = card[:-1]  # Remove the suit
        if card_rank in ["J", "Q", "K"]:
            value += 10
        elif card_rank == "A":
            value += 11
            aces += 1
        else:
            value += int(card_rank)
    # Handle aces
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def handle_dealer_choice(dealer):
    if dealer.get_agent_status() == "ACTIVE":
        hand_value = calculate_hand_value(dealer.get_raw_hand())
        if hand_value < 17:
            new_card = CARDS.pop()
            dealer.add_card_to_hand(new_card)
            if calculate_hand_value(dealer.get_raw_hand()) > 21:
                dealer._status = "BUST"
        else:
            dealer._status = "STAND"

def handle_agent_choice(choice, agent):
    print("handling " + str(choice) + " for agent " + str(agent.get_name()))
    if choice == "HIT":
        new_card = CARDS.pop()
        agent.add_card_to_hand(new_card)
        print(agent.get_hand())
        # Update the agent's status if needed
        # (You'll need to implement the `calculate_hand_value` function)
        if calculate_hand_value(agent.get_hand()) > 21:
            agent._status = "BUST"
    elif choice == "STAND":
        agent._status = "STAND"
    elif choice == "DOUBLE DOWN":
        print("doubling down!")
        new_card = CARDS.pop()
        agent.add_card_to_hand(new_card)
        agent._bet *= 2  # Double the bet
        agent._chips -= agent._bet  # Update the chips
        # agent._status = "STAND"  # Normally, you stand after doubling down
    elif choice == "SPLIT":
        # Implement this part as per your game logic
        pass


def run_turn_for_agent(agent, dealer, all_players, is_debug):
    print(f"{agent.get_name()}'s turn is running")
    while not agent.is_agent_done():
        print_table(dealer, *all_players)
        if agent.get_name() == "John Ferguson":  # Assuming this is your dealer's name
            handle_dealer_choice(agent)
        else:
            choice = agent.run_agent(is_debug)
            handle_agent_choice(choice, agent)

def run_full_game(game_mode):
    print("Starting a new game")
    dealer = Dealer()
    players = [
        Agent1("Agent_1 (AI)"),
        Agent2("Agent_2 (AI)"),
        Agent3("Agent_3 (AI)"),
        Agent1("Agent_4 (AI)"),
        Agent2("Agent_5 (AI)"),
        Agent3("Agent_6 (AI)")
    ]
    
    is_debug = game_mode == "debug"

    print("Initializing deck of cards")
    CARDS = initialize_cards_randomly()

    print("Shuffling deck of cards")
    shuffle_cards()

    print("Dealing out initial cards")
    deal_cards(dealer, *players, is_debug=is_debug)

    for player in players:
        run_turn_for_agent(player, dealer, players, is_debug)
        
    run_turn_for_agent(dealer, dealer, players, is_debug)
    
    print("Ending game")


def main():
    requested_exit = False
    game_mode = ""
    simulation_iterations = 0
    max_simulation_iterations = 1000

    print("Do you want to run in debug or simulation mode?")
    mode = input("Type 1 for debug, 2 for simulation\n")

    if mode == "1":
        game_mode = "debug"
    elif mode == "2":
        game_mode = "simulation"
    else:
        print("Your input of " + mode +
              " is not a valid option. Please try again with a valid mode.")
        exit(1)

    while not requested_exit:
        command = ""
        if game_mode == "debug":
            command = input("Press any key to continue, or \"exit\" to stop\n")

        run_full_game(game_mode)

        simulation_iterations += 1
        print("Completed " + str(simulation_iterations) + " out of " + str(max_simulation_iterations) + " iterations.")
        print(str(100 * (simulation_iterations / max_simulation_iterations)) + "% Complete")

        if command == "exit" or simulation_iterations == max_simulation_iterations:
            requested_exit = True



if __name__ == "__main__":
    main()
