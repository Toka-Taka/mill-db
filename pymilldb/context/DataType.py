import logging
import abc

logger = logging.getLogger('DataType')


class BaseType(abc.ABC):
    type_name = ''

    @abc.abstractmethod
    def variable(self, name, prefix=''):
        pass

    @abc.abstractmethod
    def str_param_for_select(self, name):
        pass

    @abc.abstractmethod
    def str_column_for_select(self, name):
        pass

    @abc.abstractmethod
    def str_out(self, name):
        pass

    @abc.abstractmethod
    def signature(self, name):
        pass

    @abc.abstractmethod
    def select_expr(self, param, column):
        pass

    @abc.abstractmethod
    def compare_less_expr(self, s1, col1, s2, col2):
        pass

    @abc.abstractmethod
    def compare_greater_expr(self, s1, col1, s2, col2):
        pass


class ConstType(BaseType):
    @classmethod
    def variable(cls, name, prefix=''):
        return f'{cls.type_name} {prefix}{name}'

    @classmethod
    def str_param_for_select(cls, name):
        return cls.signature(name, 'p_')

    @classmethod
    def str_column_for_select(cls, name):
        return cls.signature(name, 'c_')

    @classmethod
    def str_out(cls, name):
        return cls.variable(name)

    @classmethod
    def signature(cls, name, prefix=''):
        return cls.variable(name, prefix)

    @classmethod
    def select_expr(cls, param, column):
        return f'inserted->{param} = c_{column};'

    @classmethod
    def cmp(cls, s1, col1, s2, col2, cmp):
        return f'({s1}->{col1} {cmp} {s2}->{col2})'

    @classmethod
    def compare_less_expr(cls, s1, col1, s2, col2):
        return cls.cmp(s1, col1, s2, col2, '<')

    @classmethod
    def compare_greater_expr(cls, s1, col1, s2, col2):
        return cls.cmp(s1, col1, s2, col2, '>')


class Int(ConstType):
    type_name = 'int32_t'


class Float(ConstType):
    type_name = 'float'


class Double(ConstType):
    type_name = 'double'


class ArrayType(BaseType):
    def __init__(self, size):
        self.size = size

    def variable(self, name, prefix=''):
        return f'{self.type_name} {name}[{self.size}]'

    def str_param_for_select(self, name):
        return self.signature(name, 'p_')

    def str_column_for_select(self, name):
        return self.signature(name, 'c_')

    def str_out(self, name):
        return self.variable(name)

    def signature(self, name, prefix=''):
        return f'const {self.type_name}* {name}'

    @abc.abstractmethod
    def select_expr(self, param, column):
        pass

    @abc.abstractmethod
    def compare_less_expr(self, s1, col1, s2, col2):
        pass

    @abc.abstractmethod
    def compare_greater_expr(self, s1, col1, s2, col2):
        pass


class Char(ArrayType):
    type_name = 'char'

    def select_expr(self, param, column):
        return (
            f'memcpy(inserted->{param}, c_{column}, {self.size});\n'
            f'inserted->{param}[{self.size}] = \'\\0\';'
        )

    def cmp(self, s1, col1, s2, col2, cmp):
        return f'strncmp({s1}->{col1}, {s2}->{col2}, {self.size}) {cmp} 0'

    def compare_less_expr(self, s1, col1, s2, col2):
        return self.cmp(s1, col1, s2, col2, '<')

    def compare_greater_expr(self, s1, col1, s2, col2):
        return self.cmp(s1, col1, s2, col2, '>')


class Sequence(BaseType):
    pass


name_to_type = {
    'INT': {'type': Int, 'has_size': False},
    'FLOAT': {'type': Float, 'has_size': False},
    'DOUBLE': {'type': Double, 'has_size': False},
    'CHAR': {'type': Char, 'has_size': True},
}


def get_type_by_name(name: str, size=None):
    name = name.upper()
    meta = name_to_type.get(name)
    if not meta:
        logger.error('Type: %s not found. Support INT, FLOAT, DOUBLE, CHAR and TEXT', name)
        return
    kind = meta['type']
    has_size = meta['has_size']
    if has_size and size is None:
        logger.error('Type %s needs size setting', name)
        return
    elif not has_size and size is not None:
        logging.warning('Type %s does not support sizing. Size ignoring', name)
        size = None
    if has_size:
        return kind(size)
    else:
        return kind
