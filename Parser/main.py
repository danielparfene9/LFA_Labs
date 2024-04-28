from Lexer import *
from AST import *
# import ast


def main():
    expression = """new classifier = new model ("DecisionTree", criterion="entropy", max_depth=5);
new regressor = new model ("RandomForestRegressor", n_estimators=100, max_depth=10);
classifier.train(X_train, y_train);
classifier.evaluate(X_test, y_test);
classifier.save_model("classifier_model.pkl");
regressor.train(X_train, y_train);
regressor.evaluate(X_test, y_test);
regressor.save_model("regressor_model.pkl");
model_loaded = load_model("classifier_model.pkl");
model_loaded.evaluate(X_test, y_test);
is_classifier = model_loaded.is_classifier();
is_regressor = regressor.is_regressor();
print("Is the loaded model a classifier?", is_classifier);
print("Is the regressor a classifier?", is_regressor);"""

    lexer = Lexer(expression)
    while True:
        token = lexer.get_next_token()
        if token.type == TokenType.EOF:
            break
        print(token)

    parser = Parser(lexer)
    ast = parser.parse()
    print(ast)

    # node = ast.parse(expression)
    # print(node)


if __name__ == '__main__':
    main()

