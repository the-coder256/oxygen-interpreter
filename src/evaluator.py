import tokeniser
import parser

default_variables = {"print": "<built-in function 'print'>",
                              "true": 1,
                              "false": 0}

class Env:    # Allows for scoping
    def __init__(self, init_values):
        self.values = init_values
    
    def get(self, name):
        return self.values.get(name)
    
    def set(self, name, value):
        self.values.update({str(name): value})
        return value

class Evaluator:
    def __init__(self):
        self.global_variables = Env(default_variables.copy())
        self.local_variables = {}   # Contains a bunch of environments
        self.current_env = "global"
    
    def is_base_type(self, value):
        value_type = type(value)
        return value_type == int or value_type == float or value_type == str
    
    def num(self, value):
        new = float(value)
        if int(value) == new:
            new = int(value)
        return new
    
    def assign(self, variable, value):
        i = variable
        if not self.is_base_type(value):
            v = self.evaluate_tree(value)
        else:
            v = value
        if self.current_env == "global":
            self.global_variables.set(i, v)
        else:
            self.local_variables.get(self.current_env).set(i, v)
    
    def get(self, name):
        if self.current_env == "global":
            value = self.global_variables.get(name)
        else:
            value = self.local_variables.get(self.current_env).get(name)

        if value == None:
            value = self.global_variables.get(name)
        if value == None:
            print("Variable '" + str(name) + "' hasn't been assigned a value")
            exit(1)
        else:
            return value

    def evaluate_tree(self, tree):
        t_tree = type(tree)
        if t_tree == parser.Call:
            if not self.is_base_type(tree.callee):
                callee = self.evaluate_tree(tree.callee)
            else:
                callee = tree.callee
            args = []
            for index in range(len(tree.arguments)):
                arg = tree.arguments[index]
                if not self.is_base_type(arg):
                    base_arg = self.evaluate_tree(arg)
                args.append(base_arg)
            
            if callee == "<built-in function 'print'>":
                print(*args)
            else:
                definition = callee
                if definition == None:
                    print("'" + str(callee.name) + "' isn't defined")
                    exit(1)
                
                # Call by 'definition', create an environment and focus on it, assign variables with name of parameters
                self.current_env = str(callee.name.value)
                self.local_variables.update({self.current_env: Env(default_variables.copy())})
                call_args = tree.arguments

                for index in range(len(definition.parameters)):
                    param_name = definition.parameters[index]
                    try:
                        call_arg = call_args[index]
                    except:
                        call_arg = ""
                    self.local_variables.get(self.current_env).set(param_name, call_arg)
                
                statemts = definition.statements

                for index in range(len(statemts)):
                    stmt = statemts[index]
                    if not self.is_base_type(stmt):
                        if type(stmt) == parser.Return:
                            if not self.is_base_type(stmt.value):
                                return_value = self.evaluate_tree(stmt.value)
                            else:
                                return_value = stmt.value
                            self.local_variables.pop(self.current_env)
                            self.current_env = "global"
                            return return_value
                        else:
                            statemts[index] = self.evaluate_tree(stmt)
                
                self.local_variables.pop(self.current_env)
                self.current_env = "global"
        elif t_tree == parser.Assign:
            ident = tree.ident
            value = tree.value
            self.assign(ident, value)
        elif t_tree == parser.Ident:
            return self.get(tree.name)
        elif t_tree == parser.IfCondition:
            if not self.is_base_type(tree.condition):
                condition = self.evaluate_tree(tree.condition)
            else:
                condition = tree.condition

            if condition:
                for index in range(len(tree.statements)):
                    stmt = tree.statements[index]
                    if not self.is_base_type(stmt):
                        base_stmt = self.evaluate_tree(stmt)
            else:
                if tree.elseif_:
                    else_ifs = tree.elseif_
                    else_blocked = False
                    for elseif in else_ifs:
                        # get the base condition
                        if not self.is_base_type(elseif.condition):
                            c = self.evaluate_tree(elseif.condition)
                        else:
                            c = elseif.condition
                        
                        # if c then run stmts and block else
                        if c:
                            stmts = elseif.statements

                            for i in range(len(stmts)):
                                s = stmts[i]
                                if not self.is_base_type(s):
                                    base_stmt = self.evaluate_tree(s)

                            else_blocked = True
                            break
                    if tree.else_ and not else_blocked:
                        for index in range(len(tree.else_.statements)):
                            else_stmt = tree.else_.statements[index]
                            if not self.is_base_type(else_stmt):
                                tree.else_.statements[index] = self.evaluate_tree(else_stmt)
                elif tree.else_:
                    for index in range(len(tree.else_.statements)):
                        else_stmt = tree.else_.statements[index]
                        if not self.is_base_type(else_stmt):
                            base_else_stmt = self.evaluate_tree(else_stmt)
        elif t_tree == parser.Definition:
            ident = tree.name.value
            value = tree
            if self.current_env == "global":
                self.global_variables.set(ident, value)
            else:
                self.local_variables.get(self.current_env).set(ident, value)
        elif t_tree == parser.BinOp:
            op = tree.op
            if not self.is_base_type(tree.num1):
                left = self.evaluate_tree(tree.num1)
            else:
                left = tree.num1
            if not self.is_base_type(tree.num2):
                right = self.evaluate_tree(tree.num2)
            else:
                right = tree.num2
            if type(op) == tokeniser.T_Plus:
                return left + right
            elif type(op) == tokeniser.T_Minus:
                return left - right
            elif type(op) == tokeniser.T_Star:
                return left * right
            elif type(op) == tokeniser.T_Slash:
                return self.num(left / right)
            else:
                print("Unknown operator '" + str(op.value) + "'")
                exit(1)
        elif t_tree == parser.For:
            variable = tree.variable

            if not self.is_base_type(tree.start):
                start = self.evaluate_tree(tree.start)
            else:
                start = tree.start
            if not self.is_base_type(tree.end):
                end = self.evaluate_tree(tree.end)
            else:
                end = tree.end
            if not self.is_base_type(tree.increment):
                increment = self.evaluate_tree(tree.increment)
            else:
                increment = tree.increment

            statements = tree.statements

            self.assign(variable, start)

            while self.get(variable) < end + 1:
                # Evaluate all expressions (single iteration)
                for idx in range(len(statements)):
                    st = tree.statements[idx]
                    if not self.is_base_type(st):
                        base_stmt = self.evaluate_tree(st)

                # Increment the variable thing
                self.assign(variable, self.get(variable) + increment)
        else:
            return tree

    def evaluate(self, trees):
        for ast in trees:
            self.evaluate_tree(ast)