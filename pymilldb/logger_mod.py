import logging
import logging.config
import os

import yaml


def setup_logging(
        default_path='logging.yaml',
        default_level=logging.DEBUG,
        env_key='LOG_CFG'
):
    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class Logger(object):
    is_crashed = False

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def __getattr__(self, item):
        if item in ('error', 'exception', 'critical', 'fatal'):
            Logger.is_crashed = True
        return getattr(self.logger, item)


_getLogger = logging.getLogger


# noinspection PyPep8Naming
def getLogger(name=None):
    return Logger(_getLogger(name))


logging.getLogger = getLogger
