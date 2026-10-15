import unittest


class MyTestCase(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_win32_controller(self):
        self.assertEqual(True, False)  #

if __name__ == '__main__':
    unittest.main()
