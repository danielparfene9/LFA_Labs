class ChomskyNormalForm:
    def __init__(self, grammar):
        self.Vn = grammar['VN']
        self.Vt = grammar['VT']
        self.P = grammar['P']
        self.S = 'S'
        new_productions = self.remove_epsilon_productions()
        self.P = new_productions
        new_productions = self.remove_unit_productions()
        self.P = new_productions
        new_productions = self.remove_inaccessible_symbols()
        self.P = new_productions
        new_productions = self.remove_non_productive_symbols()
        self.P = new_productions
        new_productions = self.to_cnf()
        self.P = new_productions

    def remove_epsilon_productions(self):
        epsilon_producing_non_terminals = set()

        for non_terminal, productions in self.P.items():
            if '' in productions:
                epsilon_producing_non_terminals.add(non_terminal)

        changes_made = True
        while changes_made:
            changes_made = False
            for non_terminal, productions in self.P.items():
                for production in productions:
                    if all(c in epsilon_producing_non_terminals or c == '' for c in production):
                        if epsilon_producing_non_terminals.add(non_terminal):
                            changes_made = True

        new_productions = {}
        for non_terminal, productions in self.P.items():
            adjusted_productions = set()
            for production in productions:
                if production != '':
                    for i in range(1 << len(production)):
                        combination = ''.join(production[j] for j in range(len(production)) if (i & (1 << j)) == 0 or self.production_contains(epsilon_producing_non_terminals, production[j]))
                        if combination:
                            adjusted_productions.add(combination)
            new_productions[non_terminal] = list(adjusted_productions)

        return new_productions

    def remove_unit_productions(self):
        result_productions = {}
        direct_unit_productions = {}

        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) == 1 and production in self.Vn:
                    direct_unit_productions.setdefault(non_terminal, []).append(production)
                else:
                    result_productions.setdefault(non_terminal, []).append(production)

        for non_terminal, unit_productions in direct_unit_productions.items():
            visited = set()
            to_visit = unit_productions[:]

            while to_visit:
                current = to_visit.pop()
                if current not in visited:
                    visited.add(current)

                    current_productions = self.P.get(current, [])
                    for prod in current_productions:
                        if len(prod) == 1 and prod in self.Vn and prod not in visited:
                            to_visit.append(prod)
                        else:
                            result_productions.setdefault(non_terminal, []).append(prod)

        return result_productions

    def remove_inaccessible_symbols(self):
        accessible_symbols = {'S'}
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.P.items():
                if non_terminal in accessible_symbols:
                    for production in productions:
                        for symbol in production:
                            if symbol in self.Vn and symbol not in accessible_symbols:
                                accessible_symbols.add(symbol)
                                changed = True

        new_vn = [s for s in self.Vn if s in accessible_symbols]
        new_productions = {non_terminal: productions for non_terminal, productions in self.P.items() if non_terminal in accessible_symbols}
        self.Vn = new_vn

        return new_productions

    def remove_non_productive_symbols(self):
        productive_symbols = set()
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.P.items():
                if non_terminal not in productive_symbols:
                    for production in productions:
                        production_is_productive = all(sym in self.Vt or sym in productive_symbols for sym in production)
                        if production_is_productive:
                            productive_symbols.add(non_terminal)
                            changed = True

        new_productions = {non_terminal: [prod for prod in productions if all(sym in self.Vt or sym in productive_symbols for sym in prod)] for non_terminal, productions in self.P.items() if non_terminal in productive_symbols}
        self.Vn = list(productive_symbols)

        return new_productions

    def to_cnf(self):
        new_productions = {}
        terminal_replacements = {}
        existing_productions = {}
        new_non_terminals = set(self.Vn)
        new_var = 'A'

        while new_var in new_non_terminals:
            new_var = chr(ord(new_var) + 1)

        for lhs, rhss in self.P.items():
            for rhs in rhss:
                if len(rhs) == 1 and rhs in self.Vt:
                    new_productions.setdefault(lhs, []).append(rhs)
                elif len(rhs) == 2 and rhs[0] in self.Vn and rhs[1] in self.Vn:
                    new_productions.setdefault(lhs, []).append(rhs)
                else:
                    modified_production = []
                    for sym in rhs:
                        if sym in self.Vt:
                            terminal_replacement = terminal_replacements.get(sym)
                            if terminal_replacement is None:
                                terminal_replacement = existing_productions.get(sym)
                                if terminal_replacement is None:
                                    terminal_replacement = new_var
                                    new_non_terminals.add(new_var)
                                    terminal_replacements[sym] = terminal_replacement
                                    existing_productions[sym] = terminal_replacement
                                    new_productions.setdefault(terminal_replacement, []).append(sym)
                                    new_var = chr(ord(new_var) + 1)
                                else:
                                    terminal_replacements[sym] = terminal_replacement
                            modified_production.append(terminal_replacement)
                        else:
                            modified_production.append(sym)

                    while len(modified_production) > 2:
                        combined_symbols = ''.join(modified_production[:2])
                        new_var_str = existing_productions.get(combined_symbols)
                        if new_var_str is None:
                            new_var_str = new_var
                            new_non_terminals.add(new_var)
                            existing_productions[combined_symbols] = new_var_str
                            new_productions[new_var_str] = [combined_symbols]
                            new_var = chr(ord(new_var) + 1)

                        modified_production = [new_var_str] + modified_production[2:]

                    new_productions.setdefault(lhs, []).append(''.join(modified_production))

        self.Vn = list(new_non_terminals)
        return new_productions

    def production_contains(self, epsilon_producing_non_terminals, symbol):
        return symbol in epsilon_producing_non_terminals or symbol == ''


grammar = {
    'VN': {'S', 'A', 'B', 'C', 'E'},
    'VT': {'a', 'd'},
    'P': {
        'S': ['dB', 'B'],
        'A': ['d', 'dS', 'aAdCB'],
        'B': ['aC', 'bA', 'AC'],
        'C': [''],
        'E': ['AS']
    }
}

cnf = ChomskyNormalForm(grammar)
print("Chomsky Normal Form Productions:")
for non_terminal, productions in cnf.P.items():
    for production in productions:
        print(non_terminal + " -> " + production)
