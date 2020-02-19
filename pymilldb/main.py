import logging
import os

import jinja2

from . import context
from . import logger_mod
from . import parser

logger_mod.setup_logging()

logger = logging.getLogger('main')


class Counter(object):
    def __init__(self, value=0):
        self.count = value

    def __call__(self):
        self.count += 1
        return self.count - 1

    def __str__(self):
        return str(self.count)


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

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('pymilldb/template'))
    env.globals['isinstance'] = isinstance
    env.globals['zip'] = zip
    env.globals['any'] = any
    env.globals['all'] = all
    c_file = env.get_template('Environment.c')
    h_file = env.get_template('Environment.h')
    with open('{}.c'.format(context.NAME), 'w') as f:
        f.write(c_file.render(context=context, counter=Counter()))
    with open('{}.h'.format(context.NAME), 'w') as f:
        f.write(h_file.render(context=context, counter=Counter()))
