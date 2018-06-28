from visitor import PrintVisitor


class Printer(PrintVisitor):
    """A simple pretty-printer class"""
    def __init__(self):
        self._indent = 0

    def print_Lambda(self, node):
        var_name = node.var.name
        indent_prev = self._indent
        self._indent = 0
        exp_str = self.print(node.exp)
        self._indent = indent_prev
        return self.indent() + 'fun ' + var_name + ' -> ' + exp_str

    def print_App(self, node):
        indent_prev = self._indent
        self._indent = 0
        left_exp = self.print(node.left_exp)
        right_exp = self.print(node.right_exp)
        self._indent = indent_prev
        return self.indent() + '(' + left_exp + ')(' + right_exp + ')'

    def print_BinOp(self, node):
        op = node.op
        indent_prev = self._indent
        self._indent = 0
        left_str = self.print(node.left_exp)
        right_str = self.print(node.right_exp)
        self._indent = indent_prev
        return self.indent() + left_str + ' ' + op + ' ' + right_str

    def print_LetIn(self, node):
        var_name = node.var.name
        indent_prev = self._indent
        self._indent = 0
        exp_str = self.print(node.exp)
        self._indent = indent_prev
        body_str = self.print(node.body)
        self._indent = indent_prev
        return self.indent() + 'let ' + var_name + \
               ' = ' + exp_str + ' in\n' + body_str

    def print_If(self, node):
        indent_prev = self._indent
        self._indent = 0
        cond_str = self.print(node.cond)
        self._indent = indent_prev + 1
        exp1_str = self.print(node.exp1)
        exp2_str = self.print(node.exp2)
        self._indent = indent_prev
        return self.indent() + 'if ' + cond_str + '\n' + \
               self.indent() + 'then {\n' + exp1_str + '\n' + \
               self.indent() + '} \n' + self.indent() + \
               'else {\n' + exp2_str + '\n' + self.indent() + '}'

    def print_While(self, node):
        indent_prev = self._indent
        self._indent = 0
        cond_str = self.print(node.cond)
        self._indent = indent_prev + 1
        block_str = self.print(node.block)
        self._indent = indent_prev
        return self.indent() + 'while ' + cond_str + \
               ' do {\n' + self.indent() + block_str + \
               '\n' + self.indent() + '}'

    def print_Ref(self, node):
        indent_prev = self._indent
        self._indent = 0
        exp = self.print(node.exp)
        self._indent = indent_prev
        return self.indent() + 'ref (' + exp + ')'

    def print_Bang(self, node):
        indent_prev = self._indent
        self._indent = 0
        var_name = self.print(node.exp)
        self._indent = indent_prev
        return self.indent() + '!' + var_name

    def print_Assign(self, node):
        indent_prev = self._indent
        self._indent = 0
        var_name = self.print(node.left_exp)
        exp_str = self.print(node.right_exp)
        self._indent = indent_prev
        return self.indent() + var_name + ' := ' + exp_str

    def print_Seq(self, node):
        indent_prev = self._indent
        self._indent = 0
        left_exp_str = self.print(node.left_exp)
        self._indent = indent_prev
        right_exp_str = self.print(node.right_exp)
        self._indent = indent_prev
        return self.indent() + left_exp_str + ';\n' + \
               right_exp_str

    def print_Num(self, node):
        return str(node.value)

    def print_Bool(self, node):
        return str(node.value)

    def print_Var(self, node):
        return node.name

    def indent(self):
        return '    ' * self._indent

    def write(self, node):
        if node is not None:
            print(self.print(node))
        else:
            raise Exception('Input AST is None')
