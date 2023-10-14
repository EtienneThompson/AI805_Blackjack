card_value_mapping = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}


def calculate_hand_value(hand):
    """Compute the hand's value, including aces."""
    value = 0
    aces = 0
    for card in hand:
        card_rank = card[:-1]  # Remove the suit
        if card_rank in card_value_mapping.keys():
            value += card_value_mapping[card_rank]
        elif card_rank == "A":
            value += 11
            aces += 1

    # Handle aces
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value
