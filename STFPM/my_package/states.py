class State(object):
    """
    Object that represents a state in a finite state machine (FSM). Transitions to new
    states are possible after inputting a new action to the FSM.
    """
    def __init__(self, transitions, final):
        """
        Initializes a state in an FSM
        :param transitions: the set of valid transitions for this state
        :param final: bool indicating whether or not this state is a final state
        """
        if not isinstance(transitions, set):
            raise TypeError("Parameter 'transitions' is not of type set.")
        self.transitions = transitions

        if not isinstance(final, bool):
            raise TypeError("Parameter 'final' is not of type bool.")
        self.final = final

    def transition(self, states, action):
        """
        Compares the provided action against the set of valid transitions for this state and returns the state
        it transitions to.
        :param: states: the set of states in the FSM
        :param action: the action to transition with
        :return: the state that this state transitions to
        """
        return states[0]


class FiniteStateMachine(object):
    def __init__(self, quintuple):
        """
        Formally defines a finite state machine (FSM) with quintuple (S0, F, S, T, A).

        S0 = Start state
        F = Final state
        S = Set of all states
        T = Set of transition functions
        A =  Input alphabet

        :param quintuple the tuple that represents that formal definition of an FSM.
        """
        self.start_state = quintuple[0]
        self.final_state = quintuple[1]
        self.states = quintuple[2]
        self.transitions = quintuple[3]
        self. alphabet = quintuple[4]

    def receive(self, action):
        return action

    def startup(self):
        self.current
