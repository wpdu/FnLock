import os
import re
import sys
import logging
from logging.handlers import TimedRotatingFileHandler


def create(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

    fmt = logging.Formatter('%(asctime)s %(thread)d %(levelname)s [%(module)s:%(funcName)s] %(message)s')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(fmt)

    file_handler = logging.FileHandler('cache/log.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    time_rotate_handler = TimedRotatingFileHandler('cache/log.log', when='D', backupCount=7)
    time_rotate_handler.setLevel(logging.DEBUG)
    time_rotate_handler.setFormatter(fmt)
    time_rotate_handler.suffix = '%Y-%m-%d.log'
    time_rotate_handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log$')

    err_handler = logging.FileHandler('cache/err.log')
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(fmt)

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(time_rotate_handler)
    logger.addHandler(err_handler)
    return logger


logger = create('cache')


if __name__ == "__main__":
    logger.debug('debug')
    logger.info('info')
    logger.error('error')
