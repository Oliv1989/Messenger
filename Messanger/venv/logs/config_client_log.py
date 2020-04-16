"""Client Logger  Config"""

import sys
import os
import logging
from common.variables import LOGGING_LEVEL
sys.path.append('../')

CLNT_FORMATTER = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

ONLINE_HANDLER = logging.StreamHandler(sys.stderr)
ONLINE_HANDLER.setFormatter(CLNT_FORMATTER)
# logging_level: 0-NOTSET, 10-DEBUG, 20-INFO, 30-WARNING, 40-ERROR, 50-CRITICAL
ONLINE_HANDLER.setLevel(logging.ERROR)
CLNT_LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
CLNT_LOG_FILE.setFormatter(CLNT_FORMATTER)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(ONLINE_HANDLER)
LOGGER.addHandler(CLNT_LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение об неисправности')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
