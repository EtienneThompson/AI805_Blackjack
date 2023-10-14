from enum import Enum


class AgentStates(Enum):
    ACTIVE = "ACTIVE"
    STAND = "STAND"
    BUST = "BUST"
    HIT = "HIT"
    DOUBLE_DOWN = "DOUBLE DOWN"
    SPLIT = "SPLIT"
