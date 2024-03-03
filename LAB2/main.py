from Grammar import Grammar
from FiniteAutomaton import FiniteAutomaton


class Main:
    @staticmethod
    def run():

        grammar = Grammar()
        grammar.classify_grammar()

        print("///////////////////////////////////////////////////////////////////////////////")

        fa = FiniteAutomaton()

        nfa_transition_table = fa.nfa_to_transition_table()

        print("NFA Transition Table:")
        for key, value in nfa_transition_table.items():
            if value != set():
                print(key, '->', value)

        dfa_start_state = fa.get_dfa_start_state()
        print("DFA_Start_State:", dfa_start_state, "\n")

        print("DFA_Transition_Table: \n")
        fa.print_dfa_transition_table()

        print("NFA to Regular Grammar:")

        fa.to_regular_grammar()

        if fa.is_deterministic():
            print("The Finite Automaton is deterministic.")
        else:
            print("The Finite Automaton is non-deterministic.")

        fa.visualize_automaton()
        fa.visualize_dfa()


if __name__ == "__main__":
    Main.run()

