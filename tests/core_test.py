from .context import yaftp, TESTDIR
import os
import threading
from time import sleep

import unittest

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.server = yaftp.YAFTPServer(('127.0.0.1', 2222), os.path.join(TESTDIR, 'test_folder/'))
        self.server_thread = threading.Thread(target=self.server.serve, daemon=True)  # exit when test suit end
        self.server_thread.start()


    def tearDown(self):
        pass

    def test_dir(self):
        with yaftp.YAFTP(('127.0.0.1', 2222), user='ofey', passwd='gogogo') as y:
            y.login()
            print(y.dir())



if __name__ == '__main__':
    unittest.main()
