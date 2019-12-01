import logging


def log(logger=logging, level=logging.DEBUG, name=None):
    def decorator(func):
        def new_func(*args, **kwargs):
            logger.log(level, 'Start parse %s', func.__name__ if name is None else name)
            out = func(*args, **kwargs)
            logger.log(level, 'End parse %s', func.__name__ if name is None else name)
            return out
        return new_func
    return decorator
