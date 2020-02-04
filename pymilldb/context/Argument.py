import abc


class Argument(abc.ABC):
    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def print(self):
        pass

    @abc.abstractmethod
    def signature(self):
        pass


class ArgumentParameter(Argument):
    def __init__(self, name, parameter=None):
        super().__init__(name)
        self.parameter = parameter

    @property
    def print(self):
        return

    @property
    def signature(self):
        return self.parameter.signature


class ArgumentValue(Argument):
    @property
    def print(self):
        return

    @property
    def signature(self):
        return


class ArgumentSequenceCurrent(Argument):
    def __init__(self, name, sequence=None):
        super().__init__(name)
        self.sequence = sequence

    @property
    def print(self):
        return

    @property
    def signature(self):
        return


class ArgumentSequenceNext(Argument):
    def __init__(self, name, sequence=None):
        super().__init__(name)
        self.sequence = sequence

    @property
    def print(self):
        return

    @property
    def signature(self):
        return
