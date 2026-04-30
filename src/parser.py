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
    def __init__(self, condition, statements, elseif_ = None, else_ = None):
        self.condition = condition
        self.statements = statements
        self.elseif_ = elseif_
        self.else_ = else_
class Definition:
    def __init__(self, name, parameters, statements):
        self.name = name
        self.parameters = parameters
        self.statements = statements
class Else:
    def __init__(self, statements):
        self.statements = statements
class Return:
    def __init__(self, value):
        self.value = value
class BinOp:
    def __init__(self, op, num1, num2):
        self.op = op
        self.num1 = num1
        self.num2 = num2
class ElseIf:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements
class For:
    def __init__(self, variable, start, end, increment, statements):
        self.variable = variable
        self.start = start
        self.end = end
        self.increment = increment
        self.statements = statements
class While:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements
class Break:
    pass
class Continue:
    pass
class CompoundBinOp:
    def __init__(self, op, ident, value):
        self.op = op
        self.ident = ident
        self.value = value
class Increment:
    def __init__(self, ident):
        self.ident = ident
class Decrement:
    def __init__(self, ident):
        self.ident = ident

math_toks = [
    tokeniser.T_Plus,
    tokeniser.T_Minus,
    tokeniser.T_Star,
    tokeniser.T_Slash
]

bool_expr_toks = [
    tokeniser.T_DoubleEquals,
    tokeniser.T_Less,
    tokeniser.T_Greater,
    tokeniser.T_LessEquals,
    tokeniser.T_GreaterEquals
]

compound_toks = [
    tokeniser.T_PlusEquals,
    tokeniser.T_MinusEquals,
    tokeniser.T_StarEquals,
    tokeniser.T_SlashEquals
]

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
    
    def parse_factor(self):
        if type(self.consume()) == tokeniser.T_LeftParen:
            self.advance()
            expr = self.parse_expr()
            if type(self.consume()) != tokeniser.T_RightParen:
                print("Missing ')'")
                exit(1)
            return expr
        else:
            return self.parse_expr(ignore=True)
    
    def parse_term(self):
        node = self.parse_factor()

        while type(self.consume()) in [tokeniser.T_Star, tokeniser.T_Slash]:
            op = self.advance()
            right = self.parse_factor()
            node = BinOp(op, node, right)
        
        return node
    
    def parse_math_expr(self, direct = False):
        if direct:
            self.index -= 1
        node = self.parse_term()

        while type(self.consume()) in [tokeniser.T_Plus, tokeniser.T_Minus]:
            op = self.advance()
            right = self.parse_term()
            node = BinOp(op, node, right)
        
        return node
    
    def parse_bool_expr(self):
        self.index -= 1
        node = self.parse_math_expr()

        while type(self.consume()) in bool_expr_toks:
            op = self.advance()
            right = self.parse_math_expr()
            node = BinOp(op, node, right)
        
        return node
    
    def parse_expr(self, start = None, ignore = False):
        if start == None:
            start_expr = self.advance()
        else:
            start_expr = start

        if type(start_expr) == tokeniser.T_Ident:
            if type(self.consume()) == tokeniser.T_LeftParen and not start:
                return self.parse_function_call()
            elif type(self.consume()) in bool_expr_toks and not ignore:
                return self.parse_bool_expr()
            elif type(self.consume()) in math_toks and not ignore:
                return self.parse_math_expr(direct = True)
            else:
                return Ident(start_expr.value)
        else:
            if type(self.consume()) in bool_expr_toks and not ignore:
                return self.parse_bool_expr()
            elif type(self.consume()) in math_toks and not ignore:
                return self.parse_math_expr(direct = True)
            else:
                return start_expr.value

    def parse_function_call(self):
        # at '('
        callee = self.parse_expr(self.peek(-1))
        arguments = []
        self.advance()

        while self.consume().value != ")":
            if type(self.consume()) == tokeniser.T_Comma:
                print("Missing call argument before ','")
                exit(1)
            
            arg = self.parse_expr()

            if type(arg) == type(None):
                print("Expected ')'")
                exit(1)

            arguments.append(arg)
            if type(self.consume()) == tokeniser.T_Comma:
                self.advance()
                if type(self.consume()) == tokeniser.T_RightParen:
                    print("Missing call argument after ','")
                    exit(1)
        
        self.advance()
        return Call(callee, arguments)
    
    def parse_assignment(self):
        ident = self.peek(-1).value
        self.advance()
        value = self.parse_expr()

        return Assign(ident, value)
    
    def parse_if_condition(self):
        # if condition {}
        condition = self.parse_expr()
        self.advance()
        statements = []

        while type(self.consume()) != tokeniser.T_RightBrace:
            stmt = self.parse_stmt()

            if type(stmt) == type(None):
                print("Expected '}'")
                exit(1)

            statements.append(stmt)
        
        self.advance()

        else_if_branches = []

        # else if condition {}
        if type(self.advance()) == tokeniser.T_Else and type(self.consume()) == tokeniser.T_If:
            self.advance()
            while True:
                c = self.parse_expr()
                self.advance()

                s = []

                while type(self.consume()) != tokeniser.T_RightBrace:
                    stmt = self.parse_stmt()

                    if type(stmt) == type(None):
                        print("Expected '}'")
                        exit(1)

                    s.append(stmt)
                    
                else_if_branches.append(ElseIf(c, s))
                self.advance()
                self.advance()
                self.advance()
                if not (type(self.peek(-2)) == tokeniser.T_Else and type(self.peek(-1)) == tokeniser.T_If):
                    break

        else_branch = None

        if else_if_branches:
            self.index -= 2
        elif type(self.peek(-1)) == tokeniser.T_Else:
            self.index -= 1

        # Attempt to parse an else branch
        if type(self.consume()) == tokeniser.T_Else:
            self.advance()
            self.advance()

            else_statements = []

            while type(self.consume()) != tokeniser.T_RightBrace:
                stmt = self.parse_stmt()

                if type(stmt) == type(None):
                    print("Expected '}'")
                    exit(1)
                
                else_statements.append(stmt)
            
            else_branch = Else(else_statements)

        return IfCondition(condition, statements, else_if_branches, else_branch)
    
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
            if type(self.consume()) == tokeniser.T_Comma:
                self.advance()
                if type(self.consume()) == tokeniser.T_RightParen:
                    print("Missing parameter after ','")
                    exit(1)
        
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
    
    def parse_return(self):
        expr = self.parse_expr()
        return Return(expr)
    
    def parse_for(self):
        variable = self.advance().value

        if type(self.consume()) != tokeniser.T_SingleEquals:
            print("Expected '='")
            exit(1)
        
        self.advance()
        start = self.parse_expr()

        if type(self.consume()) != tokeniser.T_Comma:
            print("Expected ','")
            exit(1)
        
        self.advance()
        end = self.parse_expr()

        increment = 1
        if type(self.consume()) == tokeniser.T_Comma:
            self.advance()
            increment = self.parse_expr()
        
        self.advance()

        statements = []

        while type(self.consume()) != tokeniser.T_RightBrace:
            stmt = self.parse_stmt()

            if type(self.consume()) == type(None):
                print("Missing '}'")
                exit(1)
            
            statements.append(stmt)
        
        return For(variable, start, end, increment, statements)
    
    def parse_while(self):
        condition = self.parse_expr()
        self.advance()
        statements = []

        while type(self.consume()) != tokeniser.T_RightBrace:
            stmt = self.parse_stmt()

            if type(stmt) == type(None):
                print("Missing '}'")
            
            statements.append(stmt)
        
        return While(condition, statements)
    
    def parse_compound_operator(self):
        ident = self.peek(-1)
        operator = self.advance()
        expr = self.parse_expr()

        return CompoundBinOp(operator, ident, expr)
    
    def parse_increment(self):
        ident = self.peek(-1)
        self.advance()
        return Increment(ident)
    
    def parse_decrement(self):
        ident = self.peek(-1)
        self.advance()
        return Decrement(ident)

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
        elif type(beginning) == tokeniser.T_Return:
            return self.parse_return()
        elif type(beginning) == tokeniser.T_For:
            return self.parse_for()
        elif type(beginning) == tokeniser.T_While:
            return self.parse_while()
        elif type(beginning) == tokeniser.T_Break:
            return Break()
        elif type(beginning) == tokeniser.T_Continue:
            return Continue()
        elif type(self.consume()) in compound_toks and type(beginning) == tokeniser.T_Ident:
            return self.parse_compound_operator()
        elif type(self.consume()) == tokeniser.T_DoublePlus and type(beginning) == tokeniser.T_Ident:
            return self.parse_increment()
        elif type(self.consume()) == tokeniser.T_DoubleMinus and type(beginning) == tokeniser.T_Ident:
            return self.parse_decrement()

    def parse(self, tokens):
        self.tokens = tokens

        while not self.at_end():
            node = self.parse_stmt()
            self.tree.append(node)
        
        return self.tree