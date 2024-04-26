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

    def classify_grammar(self):
        is_regular = self.check_regular_grammar()
        is_context_free = self.check_context_free_grammar()
        is_context_sensitive = self.check_context_sensitive_grammar()

        if is_context_sensitive:
            return print("Context-sensitive Grammar")
        elif is_context_free:
            return print("Context-free Grammar")
        elif is_regular:
            return print("Regular Grammar")

    def check_regular_grammar(self):
        # Regular grammar has only productions of the form A -> aB or A -> a
        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) > 2:
                    return False
                if len(production) == 2:
                    if production[0] not in self.VT or production[1] not in self.VN:
                        return False
                if len(production) == 1:
                    if production not in self.VT:
                        return False
        return True

    def check_context_free_grammar(self):
        # Context-free grammar has productions of the form A -> w
        for non_terminal, productions in self.P.items():
            for production in productions:
                for symbol in production:
                    if symbol in self.VN and symbol not in self.VT:
                        return False
        return True

    def check_context_sensitive_grammar(self):
        # Context-sensitive grammar has productions of the form uAv -> uwv
        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) < 3:
                    return False
        return True


