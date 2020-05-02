import unittest
import json
import sys

sys.path.append("../..")
from main import app

# from app import *

class BookingTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client(self)

    def test_case1(self):
        payload = {"source":
                       {'x': 1, 'y': 0},
                   "destination":
                       {'x': 1, 'y': 1}
                   }
        expected_response = {'car_id': 1, 'total_time': 2}
        response = self.client.post('/api/book',headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        self.assertTrue(200,response.status_code)
        self.assertEqual(expected_response,json.loads(response.data))

    def test_case2(self):
        payload = {"source":
                       {'x': 1, 'y': 1},
                   "destination":
                       {'x': 5, 'y': 5}
                   }
        expected_response = {'car_id': 2, 'total_time': 10}
        response = self.client.post('/api/book',headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        self.assertTrue(200,response.status_code)
        self.assertEqual(expected_response,json.loads(response.data))

    def test_case3(self):
        payload = {"source":
                       {'x': 1, 'y': 1}
                   }
        response = self.client.post('/api/book',headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        self.assertTrue(400,response.status_code)

if __name__ == '__main__':
    unittest.main()