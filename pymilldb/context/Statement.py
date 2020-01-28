import abc
from .Table import Table
from .Argument import Argument
from .Selection import Selection


class Statement(abc.ABC):
    mode = None

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

    def __init__(self):
        self.tables = {}
        self.selections = {}
        self.conditions = {}

    def add_table(self, table: Table):
        check_name = self.tables.get(table.name)
        if check_name:
            pass
        else:
            self.tables[table.name] = {
                'index': len(self.tables),
                'has_pl_cond': False,

            }

    def add_selection(self, selection: Selection):
        pass

    def add_condition(self, condition):
        pass

    def add_selection_to_table(self, table_name, condition):
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

    def __init__(self, table):
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
