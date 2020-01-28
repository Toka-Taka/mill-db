import logging

from .Parameter import Parameter
from .Statement import Statement

logger = logging.getLogger('Procedure')


class Procedure(object):
    READ = 'READ'
    WRITE = 'WRITE'

    @property
    def is_read(self):
        return self.mode == self.READ

    @property
    def is_write(self):
        return self.mode == self.WRITE

    def set_mode_to_read(self):
        self.mode = self.READ

    def set_mode_to_write(self):
        self.mode = self.WRITE

    def __init__(self, name):
        self.name = name

        self.mode = None
        self.parameters = {}
        self.statements = []
        self._used_parameters = set()

    def add_parameter(self, parameter: Parameter):
        check_name = self.parameters.get(parameter.name)
        if check_name:
            logger.error('Procedure `%s` already has a parameter `%s`', self.name, parameter.name)
        else:
            self.parameters[parameter.name] = parameter

    def add_statement(self, statement: Statement):
        pass
