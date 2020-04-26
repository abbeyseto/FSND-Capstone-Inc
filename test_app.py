import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import patch
import requests
from app.models import setup_db, Actors, Movies
import datetime
from app import app

producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhqbTBWbUFTRGtOdEV2NC1JYm83OCJ9.eyJpc3MiOiJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE0Mzc2NTZiNjliYzBjMTJkNGIwY2IiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODc4Nzc3MDksImV4cCI6MTU4ODc0MTcwOSwiYXpwIjoicHVkYXU2bVp4ak5nck45UFYxRDBQN2ZqcFhBb2Izd1AiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOkFjdG9ycyIsImRlbGV0ZTpNb3ZpZXMiLCJnZXQ6QWN0b3JzIiwiZ2V0Ok1vdmllcyIsInBhdGNoOkFjdG9ycyIsInBhdGNoOk1vdmllcyIsInBvc3Q6QWN0b3JzIiwicG9zdDpNb3ZpZXMiXX0.SSnNjt03kNePcUghX6YYCxSPT8vqyE3Dzif4t2E8JAMbb4u8M58sTS6Z7UQQeMupJa21bxTL7zH6B_dGC_CDQu4LqCIsL7OmoZAnmjdGFSD--ILWAZOHhElK7HhY0sCUYK241Ygx_WyTx3Hp9prIB9wz1LM5jCWksSz72nEir6RNIZR4XrKQEz0Vw_jAHXf7VN95vWwzyRdwsuLM726lV3pTtuNwlmAV39c2Mbt3BCsQBiGrcww_Tp4j4B3jje21XEEjBxupo6la9aA-s8fyudE_mnkimCZUL1c65ID8MzSzv0LaQ7lVlQwoeVyxdgOlSG9GtZi4rPf9DevX7C7dgQ"
director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhqbTBWbUFTRGtOdEV2NC1JYm83OCJ9.eyJpc3MiOiJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE0MzcyZjFjYzFhYzBjMTQ2NTIxNWEiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODc4NzczODUsImV4cCI6MTU4ODc0MTM4NSwiYXpwIjoicHVkYXU2bVp4ak5nck45UFYxRDBQN2ZqcFhBb2Izd1AiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOkFjdG9ycyIsImdldDpBY3RvcnMiLCJnZXQ6TW92aWVzIiwicGF0Y2g6QWN0b3JzIiwicGF0Y2g6TW92aWVzIiwicG9zdDpBY3RvcnMiXX0.VootwcAYcbpE-6EM1JoXP80h2pVDfTAfP8VgdMoxXfqcFA2aOw9j0zNyrO0NZEc8UaSRRVH_UYz87HbvnQutXkQZYez20Y6GX-oS0grAvGIeErqj9BuNxQtB6otLq8Pv56E8a9qxrDOhxMCxe6aCJbIHS3WHySEtSrPPeU9eB6NuTIXJHtQOASVKs0BY-cuIkLf54MqABMjbPbh5_JDT0gxnFkl7rWkmxnRvsU8bI9IXKjJ51jKcqN-bgcf8nmbIuNakQRnjefw-SFNVuvB72guVAU114JtsforAdMkFudGGTs6I2b5AyPZ8cqvWM4A3GvbLwvPZdJUdeKqbECPciw"
assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhqbTBWbUFTRGtOdEV2NC1JYm83OCJ9.eyJpc3MiOiJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWE0MzZmMTFjYzFhYzBjMTQ2NTIwZDkiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL3NldG9hcHBzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODc4NzY5MjEsImV4cCI6MTU4ODc0MDkyMSwiYXpwIjoicHVkYXU2bVp4ak5nck45UFYxRDBQN2ZqcFhBb2Izd1AiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OkFjdG9ycyIsImdldDpNb3ZpZXMiXX0.FUlOY6URugrMwIpvKg_wP-BKV5p-gK1G5mI9vsEoPR0py5TL9llAwdC5FsQ39a1C8abrljSd2qOPG8sAdkFK7qfMu-68hNgLS7FaB0F49G2N3JFFtCp8oPihmtbLJM7zplEr0gYWfsyP9qomTJA4uOWA2fMNX0jEy5I-mk-tP7351ZwjhRh6zG4ilA-rH4fgYTdhBIBGFXiqmwk80i64Pk6wWDeGYqNk6LjIl764jbaxElbNNOrsY9dz8mJ-bHlc9ubZCAqp3I3xcaqcYgULnIKntktvD-w9crhLy4cOmpMBa7KPTqrX21XvavOsxlezi_5aygepvNlKvLI8Hk-qGw"

new_actor = {
    "name": "Jina Rice",
    "age": 32,
    "email": "sarah@capstone.com",
    "salary": 5000,
    "movie_ID": 2
}
new_movie = {
    'id': '2',
    'length': 100,
    'genre': 'Drama',
    'name': 'Peace keepers',
}


class CapstoneTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.user_name = "AshNelson"
        self.password = "ologinahtti1"
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@{}/{}".format(
            self.user_name,
            self.password,
            'localhost:5432',
            self.database_name)
        setup_db(
            self.app, database_path=self.app.config["SQLALCHEMY_DATABASE_URI"])

        # with self.app.app_context():
        # self.db = SQLAlchemy()
        # self.db.init_app(self.app)
        # self.db.create_all()

        def tearDown(self):
            """Executed after reach test"""
            selection = Movies.query.filter(Movies.name == 'Peace keepers').all()
            for movie in selection:
                movie.delete()
            selection = Actors.query.filter(Actors.name == 'Jina Rice').all()
            for actor in selection:
                actor.delete()
            pass

    # def test_get_Actors_assistant(self):
    #     print("*** TESTING ASSISTANT ROLE - GET ACTORS")
    #     res = self.client().get('/actors', headers={
    #         "Authorization": 'bearer '+assistant_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(body['success'], True)

    # def test_get_Movies_assistant(self):
    #     print("*** TESTING ASSISTANT ROLE - GET MOVIES")
    #     res = self.client().get('/movies', headers={
    #         "Authorization": 'bearer '+assistant_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(body['success'], True)

    # def test_get_Actors_producer(self):
    #     print("*** TESTING PRODUCER ROLE - GET ACTORS")
    #     res = self.client().get('/actors', headers={
    #         "Authorization": 'bearer '+producer_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(body['success'], True)

    # def test_get_Movies_producer(self):
    #     print("*** TESTING PRODUCER ROLE - GET MOVIES")
    #     res = self.client().get('/movies', headers={
    #         "Authorization": 'bearer '+producer_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(body['success'], True)

    # def test_get_Actors_director(self):
    #     print("*** TESTING DIRECTOR ROLE - GET ACTORS")
    #     res = self.client().get('/actors', headers={
    #         "Authorization": 'bearer '+director_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(body['success'], True)

    # def test_get_Movies_director(self):
    #     print("*** TESTING DIRECTOR ROLE - GET MOVIES")
    #     res = self.client().get('/movies', headers={
    #         "Authorization": 'bearer '+director_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(body['success'], True)

    # def test_404_wrong_endpoint_get_Actors(self):
    #     print("*** TESTING WRONG ENDPOINTS - GET ACTORS")
    #     res = self.client().get('/actorss', headers={
    #         "Authorization": 'bearer '+assistant_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(body['success'], False)

    # def test_404_wrong_endpoint_get_Movies(self):
    #     print("*** TESTING WRONG ENDPOINTS - GET MOVIES")
    #     res = self.client().get('/movi', headers={
    #         "Authorization": 'bearer '+assistant_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(body['success'], False)

    # def test_Unauthorized_Permission_NO_HEADERS_get_Actors(self):
    #     print("*** TESTING UNAUTHORIZED PERMISSION - GET ACTORS")
    #     res = self.client().get('/actors')
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['success'], False)

    # @patch('requests.post')
    def test_create_Actor(self):
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": 'Bearer '+producer_token+''},
                                 data=json.dumps(new_actor)
                                 )
        body = json.loads(res.data)
        print(body)
        actors = Actors.query.order_by(Actors.id).all()
        total_actors = len(actors)
        print("Total actors: ", total_actors)
        added_actor = actors[total_actors-1]
        print(added_actor.format())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        # Clean up
        added_actor.delete()

    def test_422_wrong_Movie_ID_create_Actor(self):
        res = self.client().post(
            '/actors',
            data={
                "name": "john",
                "age": "10",
                "salary": "3000",
                "email": "kcdskl@jcds.com",
                "movie_ID": "1000"},
            headers={"Authorization": 'bearer '+director_token}
        )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    # def test_401_Unauthorized_Permission_create_Actor(self):
    #     res = self.client().post(
    #         '/actors',
    #         data={
    #             "name": "john",
    #             "age": "10",
    #             "salary": "3000",
    #             "email": "kcdskl@jcds.com",
    #             "movie_ID": "4"},
    #         headers={"Authorization": 'bearer '+assistant_token}
    #     )
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['success'], False)

    def test_create_Movie(self):
        res = self.client().post(
            '/movies',
            data={
                "name": "john",
                "length": "10",
                "genre": "Action",
                "actor_ID": "3"},
            content_type='application/json',
            headers={"Authorization": 'bearer '+producer_token}
        )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], False)

    def test_422_wrong_Actor_ID_create_Movie(self):
        res = self.client().post(
            '/movies',
            data=new_movie,
            content_type='application/json',
            headers={"Authorization": 'bearer '+producer_token}
        )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['success'], False)

    # def test_401_Unauthorized_Permission_create_Movie(self):
    #     res = self.client().post(
    #         '/movies',
    #         data={
    #             "name": "john",
    #             "length": "10",
    #             "genre": "Action",
    #             "actor_ID": "10000"},
    #         headers={"Authorization": 'bearer '+assistant_token}
    #     )
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['success'], False)

    def test_update_Movies(self):
        res = self.client().patch(
            "/movies/2",
            data=new_movie,
            content_type='application/json',
            headers={"Authorization": "Bearer "+producer_token}
        )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], False)

    # def test_404_wrong_ID_update_Movies(self):
    #     res = self.client().patch(
    #         '/movies/1000',
    #         data={
    #             "name": "john",
    #             "length": "10",
    #             "genre": "Action"},
    #         headers={"Authorization": 'bearer '+producer_token}
    #     )
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(body['success'], False)

    # def test_401_Unauthorized_Permission_update_Movies(self):
    #     res = self.client().patch(
    #         '/movies/1',
    #         data={
    #             "name": "john",
    #             "length": "10",
    #             "genre": "Action"},
    #         headers={"Authorization": 'bearer '+assistant_token}
    #     )
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['success'], False)

    # def test_404_wrong_ID_update_Actors(self):
    #     res = self.client().patch(
    #         '/actors/1000',
    #         data={
    #             "name": "john",
    #             "age": "10",
    #             "salary": "3000",
    #             "email": "kcdskl@jcds.com"},
    #         headers={"Authorization": 'bearer '+producer_token}
    #     )
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(body['success'], False)

    # def test_422_Wrong_ID_delete_Actor(self):
    #     res = self.client().delete('/actors/1000', headers={
    #         "Authorization": 'bearer '+producer_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(body['success'], False)

    # def test_401_Unauthorized_Permission_delete_Actor(self):
    #     res = self.client().delete('/actors/1', headers={
    #         "Authorization": 'bearer '+assistant_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['success'], False)

    def test_422_Wrong_ID_delete_Movies(self):
        res = self.client().delete('/movies/1000',
        headers={
            "Authorization": 'bearer '+producer_token})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['success'], False)

    # def test_Unauthorized_Permission_delete_Movies(self):
    #     res = self.client().delete('/movies/2', headers={
    #         "Authorization": 'bearer '+assistant_token})
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['success'], False)


if __name__ == "__main__":
    unittest.main()
