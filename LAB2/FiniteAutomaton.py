import graphviz
from graphviz import Digraph


class FiniteAutomaton:
    def __init__(self):
        self.Q = {'q0', 'q1', 'q2', 'q3'}
        self.sigma = {'a', 'b', 'c'}
        self.delta = {
            ('q0', 'a'): ['q0', 'q1'],
            ('q2', 'a'): 'q2',
            ('q1', 'b'): 'q2',
            ('q2', 'c'): 'q3',
            ('q3', 'c'): 'q3',
        }
        self.q0 = 'q0'
        self.F = {'q3'}

    def to_regular_grammar(self):

        start_symbol = self.q0

        VN = self.Q

        VT = self.sigma

        P = []
        for q in self.Q:
            for a in self.sigma:
                if (q, a) in self.delta:
                    to_state = self.delta[(q, a)]
                    if isinstance(to_state, list):
                        for state in to_state:
                            P.append(f"{q} -> {a}{state}")
                    else:
                        P.append(f"{q} -> {a}{to_state}")
            if q in self.F:
                P.append(f"{q} -> ε")

        print(f"Start symbol: {start_symbol}")
        print(f"Non-terminals: {', '.join(VN)}")
        print(f"Terminals: {', '.join(VT)}")
        print("Production rules:")
        for rule in P:
            print(rule)

    def is_deterministic(self):
        for state in self.Q:
            transitions = {symbol for (s, symbol), _ in self.delta.items() if s == state}
            if len(transitions) != len(self.sigma):
                return False
        return True

    def nfa_to_transition_table(self):
        transition_table = {}

        for state in self.Q:
            for symbol in self.sigma:
                transition_table[(state, symbol)] = set()

        for key, value in self.delta.items():
            state, symbol = key
            if isinstance(value, list):
                for next_state in value:
                    transition_table[(state, symbol)].add(next_state)
            else:
                transition_table[(state, symbol)].add(value)

        return transition_table

    def get_dfa_start_state(self):
        dfa_start_state = set()

        for (state, symbol), next_state in self.delta.items():
            if isinstance(next_state, list):
                dfa_start_state.update(next_state)

        return dfa_start_state

    def dfa_transition_table(self):
        nfa_transition_table = self.nfa_to_transition_table()
        dfa_start_state = self.get_dfa_start_state()

        dfa_states = [dfa_start_state]
        unmarked_states = [dfa_start_state]
        dfa_transition = {}

        while unmarked_states:
            current_state = unmarked_states.pop(0)

            for symbol in self.sigma:
                next_state = set()

                for state in current_state:
                    next_state.update(nfa_transition_table.get((state, symbol), set()))

                dfa_transition[(tuple(current_state), symbol)] = tuple(next_state)

                if tuple(next_state) not in dfa_states:
                    dfa_states.append(tuple(next_state))
                    unmarked_states.append(tuple(next_state))

        return dfa_transition

    def print_dfa_transition_table(self):
        dfa_transition_table = self.dfa_transition_table()

        for key, value in sorted(dfa_transition_table.items()):
            if value != ():
                print(f"{key} -> {value}")

    def visualize_automaton(self):
        dot = graphviz.Digraph(comment='Finite Automaton')

        for state in self.Q:
            if state in self.F:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')

        for transition, to_state in self.delta.items():
            from_state, symbol = transition
            if isinstance(to_state, list):
                for state in to_state:
                    dot.edge(from_state, state, label=symbol)
            else:
                dot.edge(from_state, to_state, label=symbol)

        dot.render('finite_automaton', format='png', cleanup=True)
        print("Automaton visualization saved as 'finite_automaton.png'")

    def visualize_dfa(self):
        dot = graphviz.Digraph(comment='Deterministic Finite Automaton')

        dfa_transition_table = self.dfa_transition_table()

        for transition, to_state in dfa_transition_table.items():
            from_state, symbol = transition
            dot.edge(str(from_state), str(to_state), label=symbol)

        dot.render('dfa_automaton', format='png', cleanup=True)
        print("DFA visualization saved as 'dfa_automaton.png'")
