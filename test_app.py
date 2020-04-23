import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies


class CapstoneTest(unittest.TestCase):
    def setUp(self):
        self.token_assistant = os.environ['assistant_token']
        self.token_director = os.environ['director_token']
        self.token_producer = os.environ['producer_token']
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.user_name = "postgres"
        self.password = "postgres"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.user_name,
            self.password,
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_Unauthorized_Permission_NO_HEADERS_get_Actors(self):
        res = self.client().get('/Actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_get_Actors(self):
        res = self.client().get('/Actors', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_endpoint_get_Actors(self):
        res = self.client().get('/Actorss', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_get_Movies(self):
        res = self.client().get('/Movies', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_endpoint_get_Movies(self):
        res = self.client().get('/Movi', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_delete_Actor(self):
        res = self.client().delete('/Actors/1', headers={
            "Authorization": 'bearer '+self.token_producer})
        body = json.loads(res.data)
        ques = Actors.query.filter_by(id=1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(ques, None)

    def test_422_Wrong_ID_delete_Actor(self):
        res = self.client().delete('/Actors/1000', headers={
            "Authorization": 'bearer '+self.token_producer})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['success'], False)

    def test_401_Unauthorized_Permission_delete_Actor(self):
        res = self.client().delete('/Actors/1', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_delete_Movie(self):
        res = self.client().delete('Movies/1', headers={
            "Authorization": 'bearer '+self.token_producer})
        body = json.loads(res.data)
        ques = Movies.query.filter_by(id=1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(ques, None)

    def test_422_Wrong_ID_delete_Movies(self):
        res = self.client().delete('/Movies/1000', headers={
            "Authorization": 'bearer '+self.token_producer})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['success'], False)

    def test_Unauthorized_Permission_delete_Movies(self):
        res = self.client().delete('/Movies/1', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_create_Actor(self):
        res = self.client().post(
            '/Actors',
            json={
                "name": "john",
                "age": "10",
                "salary": "3000",
                "email": "kcdskl@jcds.com",
                "movie_ID": "2"},
            headers={"Authorization": 'bearer '+self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_422_wrong_Movie_ID_create_Actor(self):
        res = self.client().post(
            '/Actors',
            json={
                "name": "john",
                "age": "10",
                "salary": "3000",
                "email": "kcdskl@jcds.com",
                "movie_ID": "1000"},
            headers={"Authorization": 'bearer '+self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_401_Unauthorized_Permission_create_Actor(self):
        res = self.client().post(
            '/Actors',
            json={
                "name": "john",
                "age": "10",
                "salary": "3000",
                "email": "kcdskl@jcds.com",
                "movie_ID": "4"},
            headers={"Authorization": 'bearer '+self.token_assistant}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_create_Movie(self):
        res = self.client().post(
            '/Movies',
            json={
                "name": "john",
                "length": "10",
                "genre": "Action",
                "actor_ID": "3"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_422_wrong_Actor_ID_create_Movie(self):
        res = self.client().post(
            '/Movies',
            json={
                "name": "john",
                "length": "10",
                "genre": "Action",
                "actor_ID": "10000"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_401_Unauthorized_Permission_create_Movie(self):
        res = self.client().post(
            '/Movies',
            json={
                "name": "john",
                "length": "10",
                "genre": "Action",
                "actor_ID": "10000"},
            headers={"Authorization": 'bearer '+self.token_assistant}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_update_Movies(self):
        res = self.client().patch(
            '/Movies/2',
            json={
                "name": "john",
                "length": "10",
                "genre": "Action"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_ID_update_Movies(self):
        res = self.client().patch(
            '/Movies/1000',
            json={
                "name": "john",
                "length": "10",
                "genre": "Action"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_401_Unauthorized_Permission_update_Movies(self):
        res = self.client().patch(
            '/Movies/1000',
            json={
                "name": "john",
                "length": "10",
                "genre": "Action"},
            headers={"Authorization": 'bearer '+self.token_assistant}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_update_Actors(self):
        res = self.client().patch(
            '/Actors/3',
            json={
                "name": "john",
                "age": "10",
                "salary": "3000",
                "email": "kcdskl@jcds.com"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_ID_update_Actors(self):
        res = self.client().patch(
            '/Actors/1000',
            json={
                "name": "john",
                "age": "10",
                "salary": "3000",
                "email": "kcdskl@jcds.com"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)


if __name__ == "__main__":
    unittest.main()
