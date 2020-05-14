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

    def test_404_get_actors(self):
        response = self.client.get('/aktor')
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 404)

    def test_create_actor(self):
        test_actor = {
            "name": "Sandra Bullock",
            "age": 45,
            "gender": "Non-binary"
        }
        response = self.client.post('/actors', json=test_actor)
        data = json.loads(response.data)
        # assert that data actors list is not empty
        self.assertTrue(len(data['actor']))
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_create_actor(self):
        test_actor = {}
        response = self.client.post('/actors', json=test_actor)
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()