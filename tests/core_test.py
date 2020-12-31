from .context import yaftp, TESTDIR
import os
import threading
from time import sleep
from threading import Lock

import unittest

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.server = yaftp.YAFTPServer(('127.0.0.1', 2222), os.path.join(TESTDIR, 'test_folder/'))
        self.server_thread = threading.Thread()  # exit when test suit end
        self.server_thread.start()
        self.server_lock = Lock()


    def tearDown(self):
        with self.server_lock:
            self.server.close_all()
        

    def test_dir(self):
        with yaftp.YAFTP(('127.0.0.1', 2222), user='ofey', passwd='gogogo') as y:
            y.login()
            print(y.dir())



if __name__ == '__main__':
    unittest.main()
