import logging


# noinspection PyPep8Naming
class log:
    size = 0
    step = 2

    def __init__(self, logger=logging, level=logging.DEBUG, name=None):
        self.logger = logger
        self.level = level
        self.name = name

    def __call__(self, func):
        def new_func(*args, **kwargs):
            self.logger.log(self.level, '%s> %s', ' ' * log.size, func.__name__ if self.name is None else self.name)
            log.size += log.step
            out = func(*args, **kwargs)
            log.size -= log.step
            self.logger.log(self.level, '%s< %s', ' ' * log.size, func.__name__ if self.name is None else self.name)
            return out
        return new_func
