"""Unit-test client"""
import sys
import os
import unittest
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import pack_presence, unpack_answ
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestClass(unittest.TestCase):
    '''
    Class for testing a client`s functions
    '''

    def test_def_presense(self):
        """The request is haved test"""
        test = pack_presence()
        test[TIME] = 1.1
        self.assertEqual(
            test, {
                ACTION: PRESENCE, TIME: 1.1, USER: {
                    ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        """The 200 answer request test"""
        self.assertEqual(unpack_answ({RESPONSE: 200}), '200 : OK')

    def test_400_ans(self):
        """The 400 answer request test"""
        self.assertEqual(unpack_answ(
            {RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """The execption in request test"""
        self.assertRaises(ValueError, unpack_answ, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
