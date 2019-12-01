import logging

from .Column import Column

logger = logging.getLogger('Table')


class Table(object):
    def __init__(self, name: str) -> None:
        self.name = name
        self.columns = {}
        self.indices = {}
        self.meta = {}
        self.pk_column = None

        self.__template = ''

    def check_column(self, name: str) -> bool:
        return name in self.columns

    def add_column(self, column: Column):
        # todo: Проверка на несколько pk?
        column_name = column.name
        if column_name in self.columns:
            logger.error(
                'The column `%s` already exists in the table %s',
                column_name, self.name
            )
        elif column.is_pk and self.pk_column is not None:
            logger.error('Not support multi PK')
        else:
            if column.is_pk:
                self.pk_column = column
            self.columns[column_name] = column

    def print_tree_node(self):
        return f"""
struct {self.name}_tree_item {{
    
}}
        """
