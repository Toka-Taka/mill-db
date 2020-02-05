import abc
import logging

from .Selection import Selection
from .Table import Table

logger = logging.getLogger('Statement')


class Statement(abc.ABC):
    mode = None

    def __init__(self, procedure):
        self.procedure = procedure

    @abc.abstractmethod
    def print(self, procedure_name):
        pass

    @abc.abstractmethod
    def print_full_signature(self, procedure_name):
        pass

    @abc.abstractmethod
    def print_arguments(self):
        pass

    @abc.abstractmethod
    def print_dependencies(self):
        pass


class SelectStatement(Statement):
    mode = 'SELECT'

    def __init__(self, procedure):
        super().__init__(procedure)

        self.tables = {}
        self.selections = []
        self.raw_selections = []
        self.conditions = {}

    def add_table(self, table: Table):
        check_name = self.tables.get(table.name)
        if check_name:
            logger.error('Table %s is already used', table.name)
        else:
            self.tables[table.name] = {
                'table': table,
                'index': len(self.tables),
                'has_pl_cond': False,
                'conditions': [],
            }

    def check_selections(self):
        for column_name, parameter in self.raw_selections:
            tables = [
                (table, column)

                for data in self.tables.values()
                for table in [data['table']]
                for column in [table.columns.get(column_name)]
                if column
            ]
            if len(tables) > 1:
                logger.error('Found many tables containing column %s', column_name)
                table, column = tables[0]
            elif len(tables) == 1:
                table, column = tables[0]
            else:
                logger.error('Not found table containing column %s', column_name)
                continue
            if column.kind != parameter.kind:
                logger.error('Incompatible types parameter %s and column %s', column.name, parameter.name)
            selection = Selection(column, parameter)
            self.selections.append(selection)

    def add_condition(self, condition):
        pass

    def add_condition_to_table(self, table_name, condition):
        pass

    def print(self, procedure_name):
        pass

    def print_full_signature(self, procedure_name):
        pass

    @property
    def print_arguments(self):
        return

    @property
    def print_dependencies(self):
        return


class InsertStatement(Statement):
    mode = 'INSERT'

    def __init__(self, procedure, table):
        super().__init__(procedure)

        self.table = table
        self.arguments = []

    def print(self, procedure_name):
        pass

    def print_full_signature(self, procedure_name):
        pass

    @property
    def print_arguments(self):
        return

    @property
    def print_dependencies(self):
        return
