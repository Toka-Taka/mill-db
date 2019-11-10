from .Types import BaseType


class Column(object):
    def __init__(self, name: str, kind: BaseType, is_pk=False):
        self.name = name
        self.kind = kind
        self.is_pk = is_pk
