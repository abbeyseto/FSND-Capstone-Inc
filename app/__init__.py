import os
from flask import Flask, abort, json, jsonify, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.models import setup_db, Actors, Movies
from app.auth import AuthError, requires_auth
import requests


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,PATCH')
        return response

    @app.route('/login')
    def login():
        return redirect("https://setoapps.auth0.com/authorize?&"
                        "audience=capstone&response_type=code&"
                        "client_id=pudau6mZxjNgrN9PV1D0P7fjpXAob3wP&"
                        "redirect_uri=http://127.0.0.1:5000/authenticate&"
                        "scope=openid%20profile%20email&state=xyzABC123")

    @app.route('/authenticate')
    def authenticate():
        headers = request.headers
        print('HEADER IS', headers)
        code = request.args.get('code')
        url = "https://setoapps.auth0.com/oauth/token"
        payload = "grant_type=authorization_code&"\
            "client_id=pudau6mZxjNgrN9PV1D0P7fjpXAob3wP&"\
            "client_secret=9S_Cl3Vp1c4jfeaGhQHHFXkTepKw"\
            "ndLwXR_bzi78FS_rHtAD2M9yAIK-XTbKJBve&"\
            "code=" + code+"&redirect_uri=http://127.0.0.1:5000/"
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=payload, headers=headers)
        data = response.json()
        print('DATA', data)
        token = data.get('access_token')
        return json.dumps(data)

    @app.route('/')
    def welcome():
        return render_template('index.html')

    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:Actors')
    def get_Actors(payload):
        '''
        This endpoint is responsible for returning all Actors from DB
        '''
        actors = Actors.query.all()
        act_format = [act.format() for act in actors]
        result = {
            "success": True,
            "Actors": act_format
        }
        print(result)
        return jsonify(result)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:Actors')
    def delete_Actors(payload, id):
        '''
        This endpoint delete Actor given his ID
        '''
        try:
            act = Actors.query.filter_by(id=id).one_or_none()
            act.delete()
            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:Actors')
    def insert_Actors(payload):
        '''
        This endpoint insert Actor information
        '''
        body = request.get_json()
        try:
            actor = Actors(
                name=body['name'],
                age=body['age'],
                email=body['email'],
                salary=body['salary'])
            movies = Movies.query.filter(
                Movies.id == body['movie_ID']).one_or_none()
            if movies:
                actor.movies = [movies]
                actor.insert()
            else:
                # actor.movies.append(movies_id=body['movie_ID'])
                actor.insert()
            return jsonify({
                'success': True
            })
        except Exception:
            abort(404)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:Actors')
    def update_Actors(payload, id):
        '''
        This endpoint updates an actor info given his id
        '''
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()
        if body['name']:
            actor.name = body['name']
        if body['age']:
            actor.age = body['age']
        if body['email']:
            actor.email = body['email']
        if body['salary']:
            actor.salary = body['salary']
        actor.update()
        return jsonify({
            'success': True,
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:Movies')
    def get_Movies(payload):
        '''
        This endpoint is responsible for returning all Movies from DB
        '''
        movies = Movies.query.all()
        mov_format = [mov.format() for mov in movies]
        result = {
            "success": True,
            "Movies": mov_format
        }
        return jsonify(result)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:Movies')
    def delete_Movies(payload, id):
        '''
        This endpoint delete Movie given his ID
        '''
        try:
            found_movies = Movies.query.filter_by(id=id).all()
            if found_movies:
                found_movies.delete()
            else:
                abort(422)
            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:Movies')
    def insert_Movies(payload):
        '''
        This endpoint insert Movie information
        '''
        body = request.get_json()
        try:
            movie = Movies(
                name=body['name'],
                length=body['length'],
                genre=body['genre'])
            actors = Actors.query.filter(
                Actors.id == body['actor_ID']).one_or_none()
            if actors:
                movie.Actors = [actors]
                movie.insert()
            else:
                movie.insert()
            return jsonify({
                'success': True
            }, 200)
        except Exception:
            abort(404)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:Movies')
    def update_Movies(payload, id):
        '''
        This endpoint updates a movie given it's id
        '''
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        if body['name']:
            movie.name = body['name']
        if body['length']:
            movie.age = body['length']
        if  body['genre']:
            movie.email = body['genre']
        movie.update()
        return jsonify({
            'success': True,
        }, 200)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'messege': "Unprocessable request"
        }), 422

    @app.errorhandler(400)
    def Bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'messege': "Bad request"
        }), 400

    @app.errorhandler(500)
    def InternalError(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def unauthorized(error):
        print(error.status_code)
        print(error.error)
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app
