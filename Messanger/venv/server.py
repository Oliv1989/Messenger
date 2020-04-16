"""Server-part"""

import socket
import sys
import logging
import time
import select
import argparse
import logs.config_server_log
from decos import log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import rcv_msg, set_off_msg

SRVR_LOGGER = logging.getLogger('server')


@log
def handling_with_clnt_msg(message, message_list, client):
    '''
    function is processing client`s messages (in-dict; out-dict)
    '''
    SRVR_LOGGER.debug(f'Получено сообщение от клиента {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        set_off_msg(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message \
            and MESSAGE_TEXT in message:
        message_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        set_off_msg(client, {RESPONSE: 400, ERROR: 'Bad Request'})
        return


@log
def arg_parser():
    """Parsing CMD arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    lstn_addr = namespace.a
    lstn_port = namespace.p

    if not 1023 < lstn_port < 65536:
        SRVR_LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{lstn_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return lstn_addr, lstn_port


def main():
    '''
    Load CMD parametrs (if none DEFAULT)
    First port to processing:
    server.py -p 8079 -a 192.168.1.2
    '''
    lstn_addr, lstn_port = arg_parser()

    SRVR_LOGGER.info(f'Запущен сервер, порт для подключений: {lstn_port}, '
                     f'адрес с которого принимаются подключения: {lstn_addr}. '
                     f'Если адрес не указан, принимаются соединения с любых адресов.')

    trnsprt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trnsprt.bind((lstn_addr, lstn_port))
    trnsprt.settimeout(0.5)

    clients = []
    messages = []

    trnsprt.listen(MAX_CONNECTIONS)

    while True:
        try:
            clnt, clnt_addr = trnsprt.accept()
        except OSError:
            pass
        else:
            SRVR_LOGGER.info(f'Установлено соединение с клиентом {clnt_addr}.')
            clients.append(clnt)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(
                    clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    handling_with_clnt_msg(
                        rcv_msg(client_with_message), messages, client_with_message)
                except BaseException:
                    SRVR_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                     f'отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    set_off_msg(waiting_client, message)
                except BaseException:
                    SRVR_LOGGER.info(
                        f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
