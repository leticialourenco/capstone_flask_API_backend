import json
import unittest
from app import app

test_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjA2NVI0TWliZ193Qm12UXY3QU01RyJ9.eyJpc3MiOiJodHRwczovL2Rldi1sZXRpY2lhbG91cmVuY28uYXV0aDAuY29tLyIsInN1YiI6ImNNRTBXZ094UnFxVDkxYkVTcDVCbXdoQjdKbHFibHdYQGNsaWVudHMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTg5NDg4OTg3LCJleHAiOjE1OTAwOTM3ODcsImF6cCI6ImNNRTBXZ094UnFxVDkxYkVTcDVCbXdoQjdKbHFibHdYIiwic2NvcGUiOiJhZGQ6YWN0b3IgZGVsZXRlOmFjdG9yIGVkaXQ6YWN0b3IgYWRkOm1vdmllIGRlbGV0ZTptb3ZpZSBlZGl0Om1vdmllIHZpZXc6bW92aWUgdmlldzphY3RvciIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImRlbGV0ZTphY3RvciIsImVkaXQ6YWN0b3IiLCJhZGQ6bW92aWUiLCJkZWxldGU6bW92aWUiLCJlZGl0Om1vdmllIiwidmlldzptb3ZpZSIsInZpZXc6YWN0b3IiXX0.KGKOMPqJ9GCOS9PnFrwU9d1nwvd8IppP2s4YU3Oxs5qHqKXRGodpP8Doppd7z7mFhwqIBeGZ7S72g_SCzeKdMkVcdB46zQ01ywcykOn13hnu-oRFF-PQIMRxeiQ61ZpIaXqFIv4DFLZCGK_XV2qC2jSyBrTYiYFsb_jzSlgdCeeToMdEO55GKxfvor1AFatJEmJsxanjKX0q23Ae5VHCtNTPQufkyOv6S3qz-bM8GUn_J3O6i2yhi-pEY0G3KmPVzx3wpi20tle_LkodG1PG0JASo3DxWPIOijj7l9O6iUHl78abLGIzw1Dl6D_JPdCtQV5PVxcBQkBOP2ZMyV5FGw"

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + test_token

    def tearDown(self):
        pass

    '''
        ACTOR TESTS
    '''
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
        response = self.client.get('/actors/123abc')
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
        self.client.delete('/actors/{}'.format(data['actor']['id']))

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
        response = self.client.patch('/actors/{}/edit'.format(id), json=test_edit)
        data = json.loads(response.data)

        # delete created actor
        self.client.delete('/actors/{}'.format(id))

        # assert that request data returned an actor
        self.assertTrue(data['actor'])
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_edit_actor(self):
        response = self.client.patch('/actors/123abc/edit')
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
        response = self.client.patch('/actors/{}/edit'.format(id), json=test_edit)
        data = json.loads(response.data)

        # delete created actor
        self.client.delete('/actors/{}'.format(id))

        # asserts that error 400 due to empty request
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

        response = self.client.delete('/actors/{}'.format(id))
        data = json.loads(response.data)
        # assert that data deleted_actor_id is not empty
        self.assertTrue(data['deleted_actor_id'])
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_actor(self):
        response = self.client.delete('/actors/123abc')
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 404)


    '''
        MOVIE TESTS
    '''
    def test_get_movies(self):
        response = self.client.get('/movies')
        data = json.loads(response.data)
        # assert that data movies list is not empty
        self.assertTrue(len(data['movies']))
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_movies(self):
        response = self.client.get('/movie')
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 404)

    def test_404_get_movie(self):
        response = self.client.get('/movies/123abc')
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 404)

    def test_create_movie(self):
        test_movie = {
            "title": "Tester Woman",
            "release_date": "1994-03-21"
        }
        response = self.client.post('/movies', json=test_movie)
        data = json.loads(response.data)

        # delete created movie
        self.client.delete('/movies/{}'.format(data['movie']['id']))

        # assert that data movie is not empty
        self.assertTrue(len(data['movie']))
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_create_movie(self):
        test_movie = {}
        response = self.client.post('/movies', json=test_movie)
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 400)

    def test_edit_movie(self):
        # create a movie to be edited
        test_movie = {
            "title": "Tester Woman",
            "release_date": "1994-03-21"
        }
        response = self.client.post('/movies', json=test_movie)
        data = json.loads(response.data)
        id = data['movie']['id']

        # create an edit request and pass a test_edit json
        test_edit = {
            "title": "Pretty Woman"
        }
        response = self.client.patch('/movies/{}/edit'.format(id), json=test_edit)
        data = json.loads(response.data)

        # delete created movie
        self.client.delete('/movies/{}'.format(id))

        # assert that request data returned an actor
        self.assertTrue(data['movie'])
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_edit_movie(self):
        response = self.client.patch('/movies/123abc/edit')
        # check response status code
        self.assertEqual(response.status_code, 404)

    def test_400_edit_movie(self):
        # create a movie to be edited
        test_movie = {
            "title": "Tester Woman",
            "release_date": "1994-03-21"
        }
        response = self.client.post('/movies', json=test_movie)
        data = json.loads(response.data)
        id = data['movie']['id']

        # create an edit request and pass a test_edit json
        test_edit = {}
        response = self.client.patch('/movies/{}/edit'.format(id), json=test_edit)
        data = json.loads(response.data)

        # delete created actor
        self.client.delete('/movies/{}'.format(id))

        # asserts that error 400 due to empty request
        self.assertEqual(response.status_code, 400)

    def test_delete_movie(self):
        # create a movie to be deleted
        test_movie = {
            "title": "Tester Woman",
            "release_date": "1994-03-21"
        }
        response = self.client.post('/movies', json=test_movie)
        data = json.loads(response.data)
        id = data['movie']['id']

        response = self.client.delete('/movies/{}'.format(id))
        data = json.loads(response.data)
        # assert that data deleted_movie_id is not empty
        self.assertTrue(data['deleted_movie_id'])
        # check response message and its code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_movie(self):
        response = self.client.delete('/movies/123abc')
        data = json.loads(response.data)
        # check response status code
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()