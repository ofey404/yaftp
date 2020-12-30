from .context import yaftp

import unittest

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        print("Setup!")

    def tearDown(self):
        print("Teardown!")

    def test_hello(self):
        y = yaftp.YAFTP()
        assert y.hello() == 0



if __name__ == '__main__':
    unittest.main()
