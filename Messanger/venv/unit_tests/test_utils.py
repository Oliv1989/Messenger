"""Unit-test utils"""

import sys
import os
import unittest
import json
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
from common.utils import rcv_msg, set_off_msg
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestSocket:
    '''
    Class TestSocket for using in main Class for testing functions
    '''
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        """
        Function is coding a message
        """
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self):
        """
        Function is decoding a message
        """
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):
    '''
    Class for testing common function
    '''
    def setUp(self):
        self.test_dict_send = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'test'
                }
            }
        self.test_dict_recv_ok = {RESPONSE: 200}
        self.test_dict_recv_err = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
            }

    def test_send_message(self):
        """
        The SET_OFF_MSG function test
        """
        test_socket = TestSocket(self.test_dict_send)
        set_off_msg(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)

    def test_get_message(self):
        """
        The RCV_MSG function test
        """
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(rcv_msg(test_sock_ok), self.test_dict_recv_ok)
        self.assertEqual(rcv_msg(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
