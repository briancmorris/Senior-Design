from enum import Enum


class ActionEnum(Enum):
    """
    Enumeration of possible contact actions. Primary use is
    for visualization and displaying action string description
    given an actionID.
    """
    SUBSCRIBE = 0
    UNSUBSCRIBE = 1
    VIEW_LINK = 2
    FORWARD_FRIEND = 3
