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

    def test_404_get_actor(self):
        response = self.client.get('/actor/123abc')
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 404)

    def test_create_actor(self):
        test_actor = {
            "name": "Sarah Jessica Tester",
            "age": 55,
            "gender": "Female"
        }
        response = self.client.post('/actors', json=test_actor)
        data = json.loads(response.data)

        # delete created actor
        self.client.delete('/actor/{}'.format(data['actor']['id']))

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

    def test_delete_actor(self):
        # create an actor to be deleted
        test_actor = {
            "name": "Sarah Jessica Tester",
            "age": 55,
            "gender": "Female"
        }
        response = self.client.post('/actors', json=test_actor)
        data = json.loads(response.data)
        id = data['actor']['id']

        response = self.client.delete('/actor/{}'.format(id))
        data = json.loads(response.data)
        # assert that data deleted_actor_id is not empty
        self.assertTrue(data['deleted_actor_id'])
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_actor(self):
        response = self.client.delete('/actor/123abc')
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 404)

    def test_edit_actor(self):
        # create an actor to be edited
        test_actor = {
            "name": "Sarah Jessica Tester",
            "age": 55,
            "gender": "Female"
        }
        response = self.client.post('/actors', json=test_actor)
        data = json.loads(response.data)
        id = data['actor']['id']

        # create an edit request and pass a test_edit json
        test_edit = {
            "name": "Sarah Jessica Parker"
        }
        response = self.client.patch('/actor/{}/edit'.format(id), json=test_edit)
        data = json.loads(response.data)

        # delete created actor
        self.client.delete('/actor/{}'.format(id))

        # assert that request data returned an actor
        self.assertTrue(data['actor'])
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_edit_actor(self):
        response = self.client.patch('/actor/123abc/edit')
        # check response status code
        self.assertEqual(response.status_code, 404)

    def test_400_edit_actor(self):
        # create an actor to be edited
        test_actor = {
            "name": "Sarah Jessica Tester",
            "age": 55,
            "gender": "Female"
        }
        response = self.client.post('/actors', json=test_actor)
        data = json.loads(response.data)
        id = data['actor']['id']

        # create an edit request and pass a test_edit json
        test_edit = {}
        response = self.client.patch('/actor/{}/edit'.format(id), json=test_edit)
        data = json.loads(response.data)

        # delete created actor
        self.client.delete('/actor/{}'.format(id))

        # asserts that error 400 due to empty request
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()