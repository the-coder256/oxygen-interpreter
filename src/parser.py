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
class IfCondition:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements
class Definition:
    def __init__(self, name, parameters, statements):
        self.name = name
        self.parameters = parameters
        self.statements = statements

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

    def at_end(self):
        return self.consume().value == "END"
    
    def parse_expr(self, start = None):
        if start == None:
            start_expr = self.advance()
        else:
            start_expr = start

        if type(start_expr) == tokeniser.T_Ident:
            return Ident(start_expr.value)
        else:
            return start_expr.value

    def parse_function_call(self):
        callee = self.parse_expr(self.peek(-1))
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
    
    def parse_if_condition(self):
        condition = self.parse_expr()
        self.advance()
        statements = []

        while type(self.consume()) != tokeniser.T_RightBrace:
            stmt = self.parse_stmt()

            if type(stmt) == type(None):
                print("Expected '}'")
                exit(1)

            statements.append(stmt)
        
        return IfCondition(condition, statements)
    
    def parse_definition(self):
        name = self.advance()

        if not type(name) == tokeniser.T_Ident:
            print("Expected function name, got '" + str(name.value) + "'")
            exit(1)
        
        self.advance()
        params = []

        while not type(self.consume()) == tokeniser.T_RightParen:
            param = self.advance()

            if type(param) == type(None):
                print("Expected ')'")
                exit(1)
            
            params.append(param.value)
        
        self.advance()
        self.advance()

        statements = []

        while not type(self.consume()) == tokeniser.T_RightBrace:
            stmt = self.parse_stmt()

            if type(stmt) == type(None):
                print("Expected '}'")
                exit(1)
            
            statements.append(stmt)
        
        self.advance()
        return Definition(name, params, statements)

    def parse_stmt(self):
        beginning = self.advance()

        if type(self.consume()) == tokeniser.T_LeftParen and type(beginning) == tokeniser.T_Ident:
            return self.parse_function_call()
        elif type(self.consume()) == tokeniser.T_SingleEquals and type(beginning) == tokeniser.T_Ident:
            return self.parse_assignment()
        elif type(beginning) == tokeniser.T_If:
            return self.parse_if_condition()
        elif type(beginning) == tokeniser.T_Define:
            return self.parse_definition()

    def parse(self, tokens):
        self.tokens = tokens

        while not self.at_end():
            node = self.parse_stmt()
            self.tree.append(node)
        
        return self.tree