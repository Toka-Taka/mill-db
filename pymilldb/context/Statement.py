import abc
from .Table import Table
from .Argument import Argument


class Statement(abc.ABC):
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
    def __init__(self, tables):
        self.tables = {}

    def add_table(self, table: Table):
        check_name = self.tables.get(table.name)
        if check_name:
            pass
        else:
            self.tables[table.name] = {
                'index': len(self.tables),
                'has_pl_cond': False,

            }

    def add_selection(self, selection):
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
    def __init__(self, table):
        self.table = table
        self.arguments = []
        self.current_value = []
        self.next_value = []

    def add_argument(self, arg: Argument):
        self.arguments.append(arg)

    def add_current_value(self, i: int, name: str):
        self.current_value[i] = name

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
