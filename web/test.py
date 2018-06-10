__author__ = 'Amit Mohapatra'

from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    def test_lookup(self):
        tester = app.test_client(self)
        response = tester.get('/urlinfo/1/127.0.0.1:8080/test?test=true')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
