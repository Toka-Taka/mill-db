import logging
from .Column import Column
logger = logging.getLogger('Table')


class Table(object):
    def __init__(self, name: str) -> None:
        self.name = name
        self.columns = {}
        self.indices = {}
        self.meta = {}

        self.__template = ''

    def check_column(self, name: str) -> bool:
        return name in self.columns

    def add_column(self, column: Column):
        # todo: Проверка на несколько pk?
        column_name = column.name
        if column_name in self.columns:
            logger.warning(
                'The column `%s` already exists in the table %s',
                column_name, self.name
            )
        else:
            self.columns[column_name] = column
