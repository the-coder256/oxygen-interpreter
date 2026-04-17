import sys
import tokeniser
import parser
import evaluator

if len(sys.argv) < 2:
    print("No file given!")
    exit(1)

if sys.argv[1] == "--version":
    print("Oxygen Intepreter v0.11")
    exit(0)

with open(sys.argv[1], "r") as file:
    content = file.read()

tokens = tokeniser.Tokeniser().tokenise(content)
tree = parser.Parser().parse(tokens)
evaluator.Evaluator().evaluate(tree)