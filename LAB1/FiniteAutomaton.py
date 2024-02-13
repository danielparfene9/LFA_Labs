class FiniteAutomaton:
    def __init__(self, grammar=None):

        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()

        # If a grammar is provided, convert it to an automaton
        if grammar:
            self.convert_from_grammar(grammar)

    def convert_from_grammar(self, grammar):

        self.states = grammar.VN
        self.alphabet = grammar.VT

        # Iterate through grammar productions
        for symbol in grammar.P:
            for production in grammar.P[symbol]:
                # If production length is 1, it's a final state transition
                if len(production) == 1:
                    self.transitions[(symbol, production)] = 'final'
                else:
                    # Otherwise, store the transition symbol
                    self.transitions[(symbol, production[0])] = production[1]

        self.initial_state = 'S'
        self.final_states = {symbol for symbol in grammar.P if symbol.isupper()}

    def check_string(self, input_string):

        current_state = self.initial_state

        # Iterate through characters in the input string
        for char in input_string:
            # Check if the current state and input character combination exists in transitions
            if (current_state, char) in self.transitions:
                # Update current state to the next state based on the transition
                current_state = self.transitions[(current_state, char)]
            else:

                return False

        return True

