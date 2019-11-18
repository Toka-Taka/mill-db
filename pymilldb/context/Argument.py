import abc
from .Parameter import Parameter
__all__ = [
    'Argument',
    'ArgumentParameter',
]


class Argument(abc.ABC):
    @abc.abstractmethod
    def print(self):
        pass

    @abc.abstractmethod
    def signature(self):
        pass


class ArgumentParameter(Argument):
    def __init__(self, parameter: Parameter):
        self.parameter = parameter

    def print(self):
        return self.parameter.name

    def signature(self):
        return self.parameter.signature()


class ArgumentValue(Argument):
    def print(self):
        pass

    def signature(self):
        pass


class ArgumentSequenceCurrent(Argument):
    def print(self):
        pass

    def signature(self):
        pass


class ArgumentSequenceNext(Argument):
    def print(self):
        pass

    def signature(self):
        pass
