import logging
import os

import jinja2

from . import context
from . import logger_mod
from . import parser

logger_mod.setup_logging()

logger = logging.getLogger('main')


def main(path):
    logger.info('Init Logger.is_crashed %s', logger_mod.Logger.is_crashed)
    name = os.path.basename(path).rsplit('.', 1)[0]
    context.NAME = name
    tok = parser.Token(open(path).read())
    par = parser.Parser(tok)
    par.program()
    logger.info('Logger.is_crashed %s', logger_mod.Logger.is_crashed)
    logger.info('context.NAME %s', context.NAME)
    logger.info('context.TABLES %s', context.TABLES)
    logger.info('context.VARIABLES %s', context.VARIABLES)

    # env = jinja2.Environment(loader=jinja2.FileSystemLoader('pymilldb/template'))
    # temp = env.get_template('Table.c')
    # with open('out.c', 'w') as f:
    #     for key, value in context.TABLES.items():
    #         f.write(temp.render(table=value, context=context))
    #         f.write('\n')
