from .Parameter import Parameter
from .Column import Column


class Selection(object):
    def __init__(self, column: Column, parameter: Parameter):
        self.column = column
        self.parameter = parameter
