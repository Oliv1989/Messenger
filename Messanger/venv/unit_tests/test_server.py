"""Unit-test server"""

import sys
import os
import unittest
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import handling_with_clnt_msg
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestServer(unittest.TestCase):
    '''
    Class for testing a server`s functions
    '''

    def setUp(self) -> None:
        self.ok_dict = {RESPONSE: 200}
        self.err_dict = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }

    def test_no_action(self):
        """The ACTION is haved in request test"""
        self.assertEqual(handling_with_clnt_msg(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        """The wrong ACTION answer in request test"""
        self.assertEqual(handling_with_clnt_msg(
            {ACTION: 'test', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        """The TIME is haved in request test"""
        self.assertEqual(handling_with_clnt_msg(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """The USER is haved in request test"""
        self.assertEqual(handling_with_clnt_msg(
            {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        """The wrong ACCOUNT_NAME in request test"""
        self.assertEqual(handling_with_clnt_msg(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Petya'}}), self.err_dict)

    def test_ok_check(self):
        """The right request test"""
        self.assertEqual(handling_with_clnt_msg(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
