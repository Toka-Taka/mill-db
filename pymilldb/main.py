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

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('pymilldb/template'))
    env.globals['isinstance'] = isinstance
    env.globals['zip'] = zip
    temp = env.get_template('Environment.c')
    with open('out.c', 'w') as f:
        f.write(temp.render(context=context))

"""
void {{ procedure.name }}_{{ loop.index }}(
{%- if procedure.is_write -%}
    {{ statement.print_full_signature(procedure.name) }}
{%- elif procedure.is_read -%}
    struct {{ procedure.name }}_out* iter
    {%- for param in procedure.parameters.values() -%}
        {%- if param.mode == 'IN' -%}
            , {{ param.signature }}
        {%- endif -%}
    {%- endfor -%}
{%- endif -%}
) {
    statement.print(procedure.name)
}
"""