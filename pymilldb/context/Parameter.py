from .DataType import BaseType


class Parameter(object):
    mode = None

    def __init__(self, name: str, kind: BaseType):
        self.name = name
        self.kind = kind

    @property
    def signature(self):
        return self.kind.signature(self.name)


class InputParameter(Parameter):
    mode = 'IN'


class OutputParameter(Parameter):
    mode = 'OUT'
