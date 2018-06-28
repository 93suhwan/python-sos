class NodeVisitor:
    """generic visitor class for operational semantics"""
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class SubVisitor:
    """generic visitor class for substitution"""
    def subst(self, node):
        method_name = 'subst_' + type(node).__name__
        substitution = getattr(self, method_name, self.generic_subst)
        return substitution(node)

    def generic_subst(self, node):
        raise Exception('No substitute_{} method'.format(type(node).__name__))


class PrintVisitor:
    """generic visitor for printing AST nodes"""
    def print(self, node):
        method_name = 'print_' + type(node).__name__
        printer = getattr(self, method_name, self.generic_print)
        return printer(node)

    def generic_print(self, node):
        raise Exception('No print_{} method'.format(type(node).__name__))
