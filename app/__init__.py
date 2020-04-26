import os
from flask import Flask, abort, json, jsonify, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.models import setup_db, Actors, Movies
from app.auth import AuthError, requires_auth
import requests


# def create_app(test_config=None):
app = Flask(__name__, instance_relative_config=False)
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
        actor = Actors.query.filter_by(id=id).one_or_none()
        if actor is None:
            return jsonify({
                "message": "actor not found",
                "error": 404
            })
        actor.delete()
    except:
        actor.end()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            "deleted_id": id
        })


@app.route('/actors', methods=['POST'])
@requires_auth(permission='post:Actors')
def insert_Actors(payload):
    '''
    This endpoint insert Actor information
    '''
    body = request.get_json()
    name = body.get('name', None)
    print(name)
    age = body.get('age', None)
    print(age)
    email = body.get('email', None)
    salary = body.get('salary', None)
    print(email)

    try:
        new_actor = Actors(name=name, age=age, email=email, salary=salary)
        new_actor.insert()
        return jsonify({
            'success': True
        })
    except:
        abort(422)


@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:Actors')
def update_Actors(payload, id):
    '''
    This endpoint updates an actor info given his id
    '''
    body = request.get_json()
    try:
        actor = Actors.query.filter_by(id=id).first()
        actor.name = body.get("name")
        actor.age = body.get("age")
        actor.gender = body.get("gender")
        actor.salary = body.get("salary")
        actor.movie_ID = body.get("movie_ID")
        actor.update()
    except:
        abort(422)
    return jsonify({
        'success': True
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
        movie = Movies.query.filter_by(id=id).one_or_none()
        if movie is None:
            return jsonify({
                "message": "movie not found",
                "error": 404
            })
        movie.delete()
    except:
        movie.end()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            "deleted_id": id
        })


@app.route('/movies', methods=['POST'])
@requires_auth(permission='post:Movies')
def insert_Movies(payload):
    '''
    This endpoint insert Movie information
    '''
    body = request.get_json()
    name = body.get('name', None)
    genre = body.get('genre', None)
    length = body.get('length', None)
    try:
        new_movie = Movies(name=name, genre=genre, length=length)
        new_movie.insert()
        return jsonify({
            'success': True
        })
    except:
        abort(422)


@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:Movies')
def update_Movies(payload, id):
    '''
    This endpoint updates a movie given it's id
    '''
    body = request.get_json()
    try:
        movie = Movies.query.filter_by(id=id).first()
        movie.name = body.get("name")
        movie.genre = body.get("genre")
        movie.length = body.get("length")
        movie.update()
    except:
        abort(422)
    return jsonify({
        'success': True
    })


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

    # return app
