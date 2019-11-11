# project/test_basic.py

import unittest
from app import api

class APITests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        pass

    # executed after each test
    def tearDown(self):
        pass

    def test_function_name(self):
        pass
        # response = self.app.get('/', follow_redirects=True)
        # self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()