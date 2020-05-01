import unittest
import json

from main import app

class BookingTestCase(unittest.TestCase):

    # def __init__(self):
    #     self.app = app.test_client()
    def case1(self):

        payload = {'x': 1, 'y': 0}, {'x': 1, 'y': 1}
        response = self.app.post('/api/book',headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        self.assertTrue(200,response.status_code)

    # def test2_createLabel_email(self):
    #     with open('input/unit_test_exec_input.json', 'r') as f:
    #         event = json.load(f)
    #     event['body-json']['accountNumber']='9999999999999999'
    #     email = Email('unit-test','unit-test-dsm-token','unit-test-trackingnumber',event['body-json'])
    #     response = email.send()
    #     self.assertEqual(json.loads(response)['status'],'Failure')
    #
    # def test3_createLabel_getShippingAddress_trial(self):
    #     address = GetShipToAddress('unit-test-dsm-token','unit-test','9999999999999999')
    #     response = address.getaddress()
    #     self.assertEqual(response['city'],'Swedesboro')
    #
    # def test4_createLabel_getShippingAddress(self):
    #     address = GetShipToAddress('unit-test-dsm-token','unit-test','8495849999999999')
    #     response = address.getaddress()
    #     self.assertEqual(response['city'].strip(),'FAIRVIEW')


if __name__ == '__main__':
    unittest.main()