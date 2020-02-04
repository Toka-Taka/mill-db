from .DataType import BaseType


class Parameter(object):
    INPUT_MODE = 'IN'
    OUTPUT_MODE = 'OUT'

    mode = None

    @property
    def is_input(self):
        return self.mode == self.INPUT_MODE

    @property
    def is_output(self):
        return self.mode == self.OUTPUT_MODE

    def __init__(self, name: str, kind: BaseType):
        self.name = name
        self.kind = kind

    @property
    def signature(self):
        return self.kind.signature(self.name)


class InputParameter(Parameter):
    mode = Parameter.INPUT_MODE


class OutputParameter(Parameter):
    mode = Parameter.OUTPUT_MODE
