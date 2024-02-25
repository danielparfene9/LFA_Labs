from Grammar import Grammar
from FiniteAutomaton import FiniteAutomaton


class Main:
    @staticmethod
    def run():

        grammar = Grammar()
        grammar.classify_grammar()

        print("///////////////////////////////////////////////////////////////////////////////")

        fa = FiniteAutomaton()
        fa.to_regular_grammar()

        if fa.is_deterministic():
            print("The Finite Automaton is deterministic.")
        else:
            print("The Finite Automaton is non-deterministic.")

        fa.visualize_automaton()


if __name__ == "__main__":
    Main.run()

