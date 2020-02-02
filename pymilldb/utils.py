import logging

size = 0
step = 2


def log(logger=logging, level=logging.DEBUG, name=None):
    def decorator(func):
        def new_func(*args, **kwargs):
            global size
            logger.log(level, '%s> %s', ' ' * size, func.__name__ if name is None else name)
            size += step
            out = func(*args, **kwargs)
            size -= step
            logger.log(level, '%s< %s', ' ' * size, func.__name__ if name is None else name)
            return out
        return new_func
    return decorator
