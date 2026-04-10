import parser

class Evaluator:
    def __init__(self):
        self.variables = {"print": "<built-in function 'print'>"}
    
    def is_base_type(self, value):
        value_type = type(value)
        return value_type == int or value_type == float or value_type == str

    def evaluate_tree(self, tree):
        t_tree = type(tree)
        if t_tree == parser.Call:
            for index in range(len(tree.arguments)):
                arg = tree.arguments[index]
                if not self.is_base_type(arg):
                    tree.arguments[index] = self.evaluate_tree(arg)
            
            if self.variables.get(tree.callee) == "<built-in function 'print'>":
                print(*tree.arguments)
        elif t_tree == parser.Assign:
            ident = tree.ident
            if not self.is_base_type(tree.value):
                value = self.evaluate_tree(tree.value)
            else:
                value = tree.value
            self.variables.update({str(ident): value})
        elif t_tree == parser.Ident:
            value = self.variables.get(tree.name)
            if value == None:
                print("Variable '" + str(tree.name) + "' hasn't been assigned a value")
                exit(1)
            else:
                return value
        else:
            return tree

    def evaluate(self, trees):
        for ast in trees:
            self.evaluate_tree(ast)