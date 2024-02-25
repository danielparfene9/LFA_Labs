import graphviz


class FiniteAutomaton:
    def __init__(self):
        self.Q = {'q0', 'q1', 'q2', 'q3'}
        self.sigma = {'a', 'b', 'c'}
        self.delta = {
            ('q0', 'a'): 'q0',
            ('q0', 'a'): 'q1',
            ('q2', 'a'): 'q2',
            ('q1', 'b'): 'q2',
            ('q2', 'c'): 'q3',
            ('q3', 'c'): 'q3',
        }
        self.q0 = 'q0'
        self.F = {'q3'}

    def to_regular_grammar(self):

        start_symbol = self.q0

        non_terminals = self.Q

        terminals = self.sigma

        production_rules = []
        for q in self.Q:
            for a in self.sigma:
                if (q, a) in self.delta:
                    to_state = self.delta[(q, a)]
                    if isinstance(to_state, list):
                        for state in to_state:
                            production_rules.append(f"{q} -> {a}{state}")
                    else:
                        production_rules.append(f"{q} -> {a}{to_state}")
            if q in self.F:
                production_rules.append(f"{q} -> ε")

        print(f"Start symbol: {start_symbol}")
        print(f"Non-terminals: {', '.join(non_terminals)}")
        print(f"Terminals: {', '.join(terminals)}")
        print("Production rules:")
        for rule in production_rules:
            print(rule)

    def is_deterministic(self):
        for state in self.Q:
            transitions = {symbol for (s, symbol), _ in self.delta.items() if s == state}
            if len(transitions) != len(self.sigma):
                return False
        return True

    def visualize_automaton(self, filename='automaton'):
        dot = graphviz.Digraph()

        for state in self.Q:
            if state in self.F:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        for (from_state, symbol), to_state in self.delta.items():
            dot.edge(from_state, to_state, label=symbol)

        dot.render(filename, format='png', cleanup=True)

        print(f"Finite Automaton visualized. Image saved as '{filename}.png'")
