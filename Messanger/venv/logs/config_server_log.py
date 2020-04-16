"""Server Logger  Config"""

import sys
import os
import logging
import logging.handlers
from common.variables import LOGGING_LEVEL
sys.path.append('../')

SRVR_FORMATTER = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

ONLINE_HANDLER = logging.StreamHandler(sys.stderr)
ONLINE_HANDLER.setFormatter(SRVR_FORMATTER)
# logging_level: 0-NOTSET, 10-DEBUG, 20-INFO, 30-WARNING, 40-ERROR, 50-CRITICAL
ONLINE_HANDLER.setLevel(logging.DEBUG)
SRVR_LOG_FILE = logging.handlers.TimedRotatingFileHandler(
    PATH, encoding='utf8', interval=1, when='D')
SRVR_LOG_FILE.setFormatter(SRVR_FORMATTER)

LOGGER = logging.getLogger('server')
LOGGER.addHandler(ONLINE_HANDLER)
LOGGER.addHandler(SRVR_LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение об неисправности')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
