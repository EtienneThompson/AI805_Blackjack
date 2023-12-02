card_value_mapping = {
    "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
}

def calculate_hand_value(hand: list) -> int:
    """Compute the hand's value, including aces."""
    value = sum(card_value_mapping.get(card[:-1], 0) for card in hand)
    aces = [card[:-1] for card in hand].count('A')
    return adjust_for_aces(value, aces)

def adjust_for_aces(value: int, aces: int) -> int:
    """Adjusts the hand value considering aces."""
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def can_split_hand(hand: list) -> bool:
    """Determines if splitting is a viable move for the given hand."""
    return len(hand) == 2 and hand[0][:-1] == hand[1][:-1]
