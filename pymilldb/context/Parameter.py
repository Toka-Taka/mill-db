from .DataType import BaseType


class Parameter(object):

    def __init__(self, name: str, kind: BaseType, mode):
        self.name = name
        self.kind = kind
        self.mode = mode

    @property
    def signature(self):
        return self.kind.signature(self.name)
