from .context import yaftp, TESTDIR
from time import sleep
from yaftp.yaftp_request import *
from .helpers import *

import unittest

class YAFTPRequestTestCase(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_parser(self):
        parser = YAFTPRequestParser()

        


if __name__ == '__main__':
    unittest.main()