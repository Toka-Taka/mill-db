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

    @property
    def print(self):
        return self.parameter.name

    @property
    def signature(self):
        return self.parameter.signature()


class ArgumentValue(Argument):
    @property
    def print(self):
        return

    @property
    def signature(self):
        return


class ArgumentSequenceCurrent(Argument):
    @property
    def print(self):
        return

    @property
    def signature(self):
        return


class ArgumentSequenceNext(Argument):
    @property
    def print(self):
        return

    @property
    def signature(self):
        return
