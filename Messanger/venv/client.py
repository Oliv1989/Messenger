"""Client-part"""

import sys
import json
import socket
import time
import argparse
import logging
import logs.config_client_log
from decos import log
from errors import ReqFieldMissingError, ServerError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import rcv_msg, set_off_msg

CLNT_LOGGER = logging.getLogger('client')


@log
def message_from_server(message):
    """Function is proccessing messages from other users"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLNT_LOGGER.info(f'Получено сообщение от пользователя '
                         f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLNT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input(
        'Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        CLNT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLNT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def pack_presence(account_name='Guest'):
    '''
    function is creating client`s out data
    '''
    out_data = {
        ACTION: PRESENCE,
        TIME: time.ctime(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLNT_LOGGER.debug(
        f'Создано {PRESENCE} сообщение для пользователя {account_name} в {time.ctime()}')
    return out_data


@log
def unpack_answ(message):
    '''
    function is describing server`s answer
    '''
    CLNT_LOGGER.debug(f'Полученное сообщение от сервера {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError


@log
def arg_parser():
    """Function is parsing CMD arguments, read parameters and return them
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    svr_addr = namespace.addr
    svr_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < svr_port < 65536:
        CLNT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {svr_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        CLNT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                             f'допустимые режимы: listen , send')
        sys.exit(1)

    return svr_addr, svr_port, client_mode


def main():
    '''Load CMD parametrs'''
    # client.py 192.168.1.2 8079
    svr_addr, svr_port, client_mode = arg_parser()

    CLNT_LOGGER.info(f'Запущен клиент с парамертами: '
                     f'адрес сервера: {svr_addr}, порт: {svr_port}')

    try:
        trnsprt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        trnsprt.connect((svr_addr, svr_port))
        set_off_msg(trnsprt, pack_presence())
        answ = unpack_answ(rcv_msg(trnsprt))
        CLNT_LOGGER.info(
            f'Установлено соединение с сервером. Ответ сервера: {answ}')
    except json.JSONDecodeError:
        CLNT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        CLNT_LOGGER.error(
            f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLNT_LOGGER.error(
            f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLNT_LOGGER.critical(
            f'Не удалось подключиться к серверу {svr_addr}:{svr_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            if client_mode == 'send':
                try:
                    set_off_msg(trnsprt, create_message(trnsprt))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLNT_LOGGER.error(
                        f'Соединение с сервером {svr_addr} было потеряно.')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    message_from_server(rcv_msg(trnsprt))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLNT_LOGGER.error(
                        f'Соединение с сервером {svr_addr} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
