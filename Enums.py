from enum import Enum

class AgentStates(Enum):
    """Represents the various states an agent (player or dealer) can be in during a blackjack game."""
    
    ACTIVE = "ACTIVE"         # The agent is actively participating in the game.
    STAND = "STAND"           # The agent has chosen to stand, taking no more cards.
    BUST = "BUST"             # The agent's hand value exceeds 21, resulting in a loss.
    HIT = "HIT"               # The agent takes another card.
    DOUBLE_DOWN = "DOUBLE_DOWN" # The agent doubles their bet and takes one final card.
    SPLIT = "SPLIT"           # The agent splits their hand into two separate hands.
