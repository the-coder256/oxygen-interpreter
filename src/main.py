import sys
import tokeniser
import parser

if len(sys.argv) < 2:
    print("No file given!")
    exit(1)

with open(sys.argv[1], "r") as file:
    content = file.read()

tokens = tokeniser.Tokeniser().tokenise(content)
tree = parser.Parser().parse(tokens)

print(tree[0].callee)
print(tree[0].arguments)