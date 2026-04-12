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

    def evaluate_tree(self, tree):
        t_tree = type(tree)
        if t_tree == parser.Call:
            if not self.is_base_type(tree.callee):
                callee = self.evaluate_tree(tree.callee)
            else:
                callee = tree.callee
            for index in range(len(tree.arguments)):
                arg = tree.arguments[index]
                if not self.is_base_type(arg):
                    tree.arguments[index] = self.evaluate_tree(arg)
            
            if callee == "<built-in function 'print'>":
                print(*tree.arguments)
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
                        call_arg = None
                    self.local_variables.get(self.current_env).set(param_name, call_arg)
                
                for index in range(len(definition.statements)):
                    stmt = definition.statements[index]
                    if not self.is_base_type(stmt):
                        definition.statements[index] = self.evaluate_tree(stmt)
                
                self.local_variables.pop(self.current_env)
                self.current_env = "global"
        elif t_tree == parser.Assign:
            ident = tree.ident
            if not self.is_base_type(tree.value):
                value = self.evaluate_tree(tree.value)
            else:
                value = tree.value
            if self.current_env == "global":
                self.global_variables.set(ident, value)
            else:
                self.local_variables.get(self.current_env).set(ident, value)
        elif t_tree == parser.Ident:
            if self.current_env == "global":
                value = self.global_variables.get(tree.name)
            else:
                value = self.local_variables.get(self.current_env).get(tree.name)

                if value == None:
                    value = self.global_variables.get(tree.name)
            if value == None:
                print("Variable '" + str(tree.name) + "' hasn't been assigned a value")
                exit(1)
            else:
                return value
        elif t_tree == parser.IfCondition:
            if not self.is_base_type(tree.condition):
                condition = self.evaluate_tree(tree.condition)
            else:
                condition = tree.condition
            
            if condition:
                for index in range(len(tree.statements)):
                    stmt = tree.statements[index]
                    if not self.is_base_type(stmt):
                        tree.statements[index] = self.evaluate_tree(stmt)
        elif t_tree == parser.Definition:
            ident = tree.name.value
            value = tree
            if self.current_env == "global":
                self.global_variables.set(ident, value)
            else:
                self.local_variables.get(self.current_env).set(ident, value)
        else:
            return tree

    def evaluate(self, trees):
        for ast in trees:
            self.evaluate_tree(ast)