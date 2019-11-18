import logging

from .Parameter import Parameter
from .Statement import Statement

logger = logging.getLogger('Procedure')


class Procedure(object):
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

        self.parameters = {}
        self.statements = {}

    def add_parameter(self, parameter: Parameter):
        check_name = self.parameters.get(parameter.name)
        if check_name:
            logger.error('Procedure `%s` already has a parameter `%s`', self.name, parameter.name)
        else:
            self.parameters[parameter.name] = parameter

    def add_statement(self, statement: Statement):
        pass

    def print(self):
        buf = ""
        buf += f"""
struct {self.name}_out_data {{
    
}};
        """
