import sys
import tokeniser

if len(sys.argv) < 2:
    print("No file given!")
    exit(1)

with open(sys.argv[1], "r") as file:
    content = file.read()

tokens = tokeniser.Tokeniser().tokenise(content)

for tok in tokens:
    print(tok.value)