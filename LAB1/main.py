import random
from Grammar import Grammar
from FiniteAutomaton import FiniteAutomaton


class Main:
    @staticmethod
    def generate_valid_strings(grammar, num_strings):
        valid_strings_with_transitions = []
        for _ in range(num_strings):
            string = ''
            transitions = [('S', 'S')]
            stack = ['S']

            while stack:
                current_symbol = stack.pop()

                if current_symbol in grammar.VT:
                    string += current_symbol
                else:
                    production = random.choice(grammar.P[current_symbol])
                    stack.extend(reversed(production))
                    transitions.append((current_symbol, production))

            valid_strings_with_transitions.append((string, transitions))
        return valid_strings_with_transitions

    @staticmethod
    def run():
        grammar = Grammar()
        finite_automaton = FiniteAutomaton()
        finite_automaton.convert_from_grammar(grammar)

        print("Generated strings:")
        valid_strings_with_transitions = Main.generate_valid_strings(grammar, 5)
        for i, (string, transitions) in enumerate(valid_strings_with_transitions, start=1):
            print(f"{i}.", end=' ')
            for j, transition in enumerate(transitions):
                if j == 0:
                    print(f"{transition[0]} -> {transition[1]}", end=' ')
                else:
                    print(f"-> {transition[1]}", end=' ')
            print(f"-> {string}")

        input_strings = ["ddc", "dabadd", "dd", "dcab", "dcad"]
        print("\nChecking if input strings are accepted by the Finite Automaton:")
        for string in input_strings:
            if finite_automaton.check_string(string):
                print(f"'{string}' is accepted by the Finite Automaton.")
            else:
                print(f"'{string}' is not accepted by the Finite Automaton.")


if __name__ == "__main__":
    Main.run()


