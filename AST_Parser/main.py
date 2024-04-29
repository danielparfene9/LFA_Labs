from lexing.lexer import Lexer
from lexing.source_line import SourceLine
from parsing.parser import Parser
from util.error import LanguageError


def main():
    print("Write your mathematical expression: ")
    lexer = Lexer()
    parser = Parser()

    while True:
        line = input("> ")
        if line == "exit": break
        if line == "": continue

        try:
            line = SourceLine(line)
            tokens = lexer.make_tokens(line)
            tree = parser.make_tree(tokens)
            print(tokens)
            print(tree)
        except LanguageError as error:
            print(error)


if __name__ == "__main__":
    main()
