# Grammar to Finite Automaton Conversion

### Course: Formal Languages & Finite Automata
### Author: Parfene Daniel FAF-222

----

## Theory

In formal language theory, there is a close relationship between grammars and automata. A grammar defines a language by generating strings, while an automaton recognizes or accepts strings from a language. The conversion from a grammar to a finite automaton enables us to verify whether a given string belongs to the language defined by the grammar.

## Objectives:

* To implement a Python program that converts a context-free grammar to a finite automaton.
* To generate valid strings based on the grammar.
* To check if input strings are accepted by the generated finite automaton.

## Implementation description

### Grammar Class:

Defines a context-free grammar with non-terminal symbols (VN), terminal symbols (VT), and production rules (P).

```python
class Grammar:
    def __init__(self):
        self.VN = {'S', 'A', 'B', 'C'}
        self.VT = {'a', 'b', 'c', 'd'}
        self.P = {
            'S': ['dA'],
            'A': ['d', 'aB'],
            'B': ['bC'],
            'C': ['cA', 'aS']
        }
```

### FiniteAutomaton Class:

Represents a finite automaton with states, alphabet, transitions, initial state, and final states. It provides methods to convert from a grammar and check strings.

```python
class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()

    def convert_from_grammar(self, grammar):
        # Implementation details omitted for brevity
        pass

    def check_string(self, input_string):
        # Implementation details omitted for brevity
        pass
```

### Main Class:

Contains methods to generate valid strings based on the grammar and to run the program.

```python
class Main:
    @staticmethod
    def generate_valid_strings(grammar, num_strings):
        # Implementation details omitted for brevity
        pass

    @staticmethod
    def run():
        # Implementation details omitted for brevity
        pass
```

### Program Execution:

The `run()` method in the `Main` class initializes a grammar, converts it to a finite automaton, generates valid strings, and checks input strings against the automaton.

## Conclusions / Screenshots / Results

The program successfully converts the grammar to a finite automaton and demonstrates the recognition of valid strings by the automaton.

## References

[1] Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation (3rd ed.). Pearson Education.
``` ````
