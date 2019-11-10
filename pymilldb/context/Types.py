class BaseType(object):
    def __init__(self, size):
        self.size = size

    def str(self):
        pass

    def str_param_for_select(self, name):
        pass

    def str_column_for_select(self, name):
        pass

    def str_out(self, name):
        pass

    def signature(self, name):
        pass

    def scan_expr(self, name):
        pass

    def init_expr(self, name):
        pass

    def select_expr(self, param, column):
        pass

    def compare_less_expr(self, s1, col1, s2, col2):
        pass

    def compare_greater_expr(self, s1, col1, s2, col2):
        pass


class Int(BaseType):
    pass


class Float(BaseType):
    pass


class Double(BaseType):
    pass


class Char(BaseType):
    pass


class Sequence(BaseType):
    pass
