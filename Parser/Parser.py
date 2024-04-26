# Define TokenType
class TokenType:
    IDENTIFIER = 'IDENTIFIER'
    KEYWORD = 'KEYWORD'
    OPERATOR = 'OPERATOR'
    LITERAL = 'LITERAL'
    PUNCTUATION = 'PUNCTUATION'

# Define keywords and operators
keywords = {'new', 'train', 'evaluate', 'save_model', 'load_model', 'is_classifier', 'is_regressor', 'print'}
operators = {'=', '(', ')', '.', ','}

# Tokenize function
def tokenize(code):
    tokens = []
    current_token = ''
    in_literal = False

    for char in code:
        if char.isspace():
            if in_literal:
                current_token += char
            else:
                if current_token:
                    tokens.append((classify_token(current_token), current_token))
                current_token = ''
        elif char in operators:
            if in_literal:
                current_token += char
            else:
                if current_token:
                    tokens.append((classify_token(current_token), current_token))
                tokens.append((TokenType.OPERATOR, char))
                current_token = ''
        elif char == '"':
            if in_literal:
                tokens.append((TokenType.LITERAL, current_token))
                current_token = ''
                in_literal = False
            else:
                in_literal = True
        else:
            current_token += char

    if current_token:
        tokens.append((classify_token(current_token), current_token))

    return tokens

# Function to classify tokens
def classify_token(token):
    if token in keywords:
        return TokenType.KEYWORD
    elif token.isdigit():
        return TokenType.LITERAL
    elif token.isalnum():
        return TokenType.IDENTIFIER
    else:
        return TokenType.PUNCTUATION

# Test tokenize function
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

tokens = tokenize(expression)
for token in tokens:
    print(token)
