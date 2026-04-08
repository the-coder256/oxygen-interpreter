import tokeniser

class Null:
    def __init__(self, value):
        self.value = value
class Call:
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

class Parser:
    def __init__(self):
        self.tokens = []
        self.index = 0
        self.tree = []
    
    def peek(self, amount = 1):
        if self.index + amount >= len(self.tokens):
            return Null(None)
        else:
            return self.tokens[self.index + amount]

    def consume(self):
        return self.tokens[self.index]

    def advance(self):
        self.index += 1
        return self.tokens[self.index - 1]
    
    def expect(self, t_type):
        if type(self.tokens[self.index]) != t_type:
            print("Expected token type " + str(t_type) + ", got " + str(type(self.tokens[self.index])))
            exit(1)

    def at_end(self):
        return self.consume().value == "END"

    def parse_function_call(self):
        callee = self.peek(-1).value
        arguments = []
        self.advance()

        while self.consume().value != ")":
            arg = self.advance().value

            if type(arg) == tokeniser.T_End:
                print("Expected ')'")
                exit(1)

            arguments.append(arg)
        
        self.advance()
        return Call(callee, arguments)

    def parse_stmt(self):
        beginning = self.advance()

        if type(self.consume()) == tokeniser.T_LeftParen and type(beginning) == tokeniser.T_Ident:
            return self.parse_function_call()

    def parse(self, tokens):
        self.tokens = tokens

        while not self.at_end():
            node = self.parse_stmt()
            self.tree.append(node)
        
        return self.tree