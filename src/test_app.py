import json
import unittest
from src.app import app

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def tearDown(self):
        pass

    def test_get_actors(self):
        response = self.client.get('/actors')
        data = json.loads(response.data)
        # assert that data actors list is not empty
        self.assertTrue(len(data['actors']))
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()