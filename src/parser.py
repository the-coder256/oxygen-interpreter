import tokeniser

class Null:
    def __init__(self, value):
        self.value = value
class Call:
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments
class Assign:
    def __init__(self, ident, value):
        self.ident = ident
        self.value = value
class Ident:
    def __init__(self, name):
        self.name = name

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
        try:
            return self.tokens[self.index]
        except:
            return Null(None)

    def advance(self):
        self.index += 1
        try:
            return self.tokens[self.index - 1]
        except:
            return Null(None)
    
    def expect(self, t_type):
        if type(self.tokens[self.index]) != t_type:
            print("Expected token type " + str(t_type) + ", got " + str(type(self.tokens[self.index])))
            exit(1)

    def at_end(self):
        return self.consume().value == "END"
    
    def parse_expr(self):
        start_expr = self.advance()

        if type(start_expr) == tokeniser.T_Ident:
            return Ident(start_expr.value)
        else:
            return start_expr.value

    def parse_function_call(self):
        callee = self.peek(-1).value
        arguments = []
        self.advance()

        while self.consume().value != ")":
            arg = self.parse_expr()

            if type(arg) == type(None):
                print("Expected ')'")
                exit(1)

            arguments.append(arg)
        
        self.advance()
        return Call(callee, arguments)
    
    def parse_assignment(self):
        ident = self.peek(-1).value
        self.advance()
        value = self.parse_expr()

        return Assign(ident, value)

    def parse_stmt(self):
        beginning = self.advance()

        if type(self.consume()) == tokeniser.T_LeftParen and type(beginning) == tokeniser.T_Ident:
            return self.parse_function_call()
        elif type(self.consume()) == tokeniser.T_SingleEquals and type(beginning) == tokeniser.T_Ident:
            return self.parse_assignment()

    def parse(self, tokens):
        self.tokens = tokens

        while not self.at_end():
            node = self.parse_stmt()
            self.tree.append(node)
        
        return self.tree