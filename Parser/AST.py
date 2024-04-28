from Lexer import TokenType


class ASTNode:
    def __str__(self, level=0):
        ret = "  " * level + str(self.__class__.__name__) + "\n"
        for child_name, child_value in vars(self).items():
            if isinstance(child_value, list):
                for child in child_value:
                    ret += child.__str__(level + 1)
            elif isinstance(child_value, ASTNode):
                ret += "  " * (level + 1) + child_name + ":\n"
                ret += child_value.__str__(level + 2)
            else:
                ret += "  " * (level + 1) + child_name + ": " + str(child_value) + "\n"
        return ret


class Num(ASTNode):
    def __init__(self, value):
        self.value = value


class String(ASTNode):
    def __init__(self, value):
        self.value = value


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class Assignment(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression


class MethodCall(ASTNode):
    def __init__(self, method_name, arguments):
        self.method_name = method_name
        self.arguments = arguments


class LoadModelCall(ASTNode):
    def __init__(self, model_name):
        self.model_name = model_name


class EvaluateCall(ASTNode):
    def __init__(self, model_name, test_data):
        self.model_name = model_name
        self.test_data = test_data


class SaveModelCall(ASTNode):
    def __init__(self, model_name, filename):
        self.model_name = model_name
        self.filename = filename


class IsClassifierCall(ASTNode):
    def __init__(self, model_name):
        self.model_name = model_name


class IsRegressorCall(ASTNode):
    def __init__(self, model_name):
        self.model_name = model_name


class PrintStatement(ASTNode):
    def __init__(self, message):
        self.message = message


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Num(token.value)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value)
        elif token.type == TokenType.IDENTIFIER:
            variable = Variable(token.value)
            self.eat(TokenType.IDENTIFIER)
            return variable
        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            return Boolean(token.value)
        elif token.type == TokenType.NEW:
            self.eat(TokenType.NEW)
            model_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.LPAREN)
            arguments = []
            while self.current_token.type != TokenType.RPAREN:
                arguments.append(self.factor())
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RPAREN)
            return MethodCall(model_name, arguments)
        else:
            self.error()

    def parse(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.IDENTIFIER:
                variable = Variable(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.ASSIGN)
                expression = self.factor()
                statements.append(Assignment(variable, expression))
            elif self.current_token.type == TokenType.NEW:
                self.eat(TokenType.NEW)
                model_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.ASSIGN)
                expression = self.factor()
                statements.append(Assignment(Variable(model_name), expression))
            elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "print":
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.LPAREN)
                message = self.current_token.value
                self.eat(TokenType.STRING)
                self.eat(TokenType.RPAREN)
                statements.append(PrintStatement(message))
            elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "load_model":
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.LPAREN)
                model_name = self.current_token.value
                self.eat(TokenType.STRING)
                self.eat(TokenType.RPAREN)
                statements.append(LoadModelCall(model_name))
            elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "evaluate":
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.LPAREN)
                model_name = self.current_token.value
                self.eat(TokenType.STRING)
                self.eat(TokenType.COMMA)
                test_data = self.factor()
                self.eat(TokenType.RPAREN)
                statements.append(EvaluateCall(model_name, test_data))
            elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "save_model":
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.LPAREN)
                model_name = self.current_token.value
                self.eat(TokenType.STRING)
                self.eat(TokenType.COMMA)
                filename = self.current_token.value
                self.eat(TokenType.STRING)
                self.eat(TokenType.RPAREN)
                statements.append(SaveModelCall(model_name, filename))
            elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "is_classifier":
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.LPAREN)
                model_name = self.current_token.value
                self.eat(TokenType.RPAREN)
                statements.append(IsClassifierCall(model_name))
            elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "is_regressor":
                self.eat(TokenType.IDENTIFIER)
                self.eat(TokenType.LPAREN)
                model_name = self.current_token.value
                self.eat(TokenType.RPAREN)
                statements.append(IsRegressorCall(model_name))
            else:
                self.error()

        return Program(statements)
