class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.keywords = {
            'new': Token('NEW'),
            'model': Token('MODEL'),
            'true': Token('BOOLEAN', True),
            'false': Token('BOOLEAN', False),
        }

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        else:
            return None

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token('NUMBER', self.integer())

            if self.current_char.isalpha() or self.current_char == '_':
                identifier = self.identifier()
                return self.keywords.get(identifier, Token('IDENTIFIER', identifier))

            if self.current_char == '"':
                return Token('STRING', self.string())

            if self.current_char == '=':
                self.advance()
                return Token('ASSIGN', '=')

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            if self.current_char == ',':
                self.advance()
                return Token('COMMA', ',')

            if self.current_char == ';':
                self.advance()
                return Token('SEMI', ';')

            if self.current_char == '.':
                self.advance()
                return Token('DOT', '.')

            self.error()

        return Token('EOF')


def main():
    expression = """new classifier = new model (" DecisionTree " , criterion =" entropy " , max_depth =5);
new regressor = new model (" RandomForestRegressor " , n_estimators =100 , max_depth =10);
classifier . train ( X_train , y_train );
classifier . evaluate ( X_test , y_test );
classifier . save_model (" classifier_model . pkl ");
regressor . train ( X_train , y_train );
regressor . evaluate ( X_test , y_test );
regressor . save_model (" regressor_model . pkl ");
model_loaded = load_model (" classifier_model . pkl ");
model_loaded . evaluate ( X_test , y_test );
is_classifier = model_loaded . is_classifier ();
is_regressor = regressor . is_regressor ();
print (" Is the loaded model a classifier ?" , is_classifier );
print (" Is the regressor a classifier ?" , is_regressor );"""
    lexer = Lexer(expression)
    while True:
        token = lexer.get_next_token()
        if token.type == 'EOF':
            break
        print(token)


if __name__ == '__main__':
    main()
