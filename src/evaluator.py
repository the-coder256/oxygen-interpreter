import parser

class Evaluator:
    def __init__(self):
        pass
    
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
            
            if tree.callee == "print":
                print(*tree.arguments)
        else:
            return tree

    def evaluate(self, trees):
        for ast in trees:
            self.evaluate_tree(ast)