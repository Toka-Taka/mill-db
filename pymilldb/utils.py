import logging
import logging.config
import os

import yaml


class MyLogger(logging.Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_crashed = False

    def error(self, msg, *args, **kwargs):
        self.is_crashed = True
        super().__init__(*args, **kwargs)

    def clear_is_crashed(self):
        self.is_crashed = False


logging.Logger = MyLogger


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
