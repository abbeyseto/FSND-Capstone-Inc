
# Capstone Agency API

This project is a web app for a casting agency (Capstone Inc.) where users can add movies, actors, and relate each actor to the movies he acted in, and vice versa. 

There are some level of permission set in this API, so depending on the kind of user, there are roles and permissions assoinged to each credentials. This project uses python, flask and postgresql for it's backend and hosted on heruko. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

No frontend is developed for this app, you can use it using cURL or [Postman](https://www.postman.com)


## Deployment & Live Testing

This API is deployed on heruko with this link as its base URL [Capstone-z Inc](https://capstonez.herokuapp.com/).

```bash
https://capstonez.herokuapp.com/
```
### Authentication
Based on the specific role you would like to test for, each of the roles has a jwt token that is available in the `setup.sh` file in the parent directory of this repository.

You will need to pass it as an Authorization header in this format

```bash
"Authorization": "Bearer ey78698ih67bjvbjkjbhjsnbahjb...."
```
*Above is just an example*

### Endpoints

- GET '/actors'
- GET '/movies'
- POST '/actors'
- POST '/movies'
- PATCH '/actors/<int:id>'
- PATCH '/movies/<int:id>'
- DELETE '/actors/<int:id>'
- DELETE '/movies/<int:id>'

Following is the demonstration of each endpoint.

- GET '/actors'
	- Fetch all Actor info from db
	- Request Argument : None
	- Returns : JSON response containing all actors with their info, and request status
	- example
		```
		{
		  "actors": [
		    {
		      "age": 38,
		      "email": "Noha@gmail.com",
		      "id": 3,
		      "movies": [
		        "GoGo",
		        "alo"
		      ],
		      "name": "Noha",
		      "salary": 1000
		    }
		  ],
		  "success": true
		}
		```

- GET '/movies'
	- Fetch all movies info from db
	- Request Argument : None
	- Returns : JSON response containing all movies with their info, and request status
	- example
		```
		{
		  "movies": [
		    {
		      "actors": [
		        "ALi",
		        "Ahmed"
		      ],
		      "genre": "Romance",
		      "id": 3,
		      "length": 1.9
		    }
		  ],
		  "success": true
		}
		```

- POST '/actors'
	- Insert Actor info into db
	- Request Argument :  `name` `email` `age` `salary` `movie_ID`
	- Returns : JSON response containing request status
	- example
		```
		{
		  "success": true
		}
		```

- POST '/movies'
	- Insert Movie info into db
	- Request Argument : `name` `length` `genre` `actor_ID`
	- Returns : JSON response containing request status
	- example
		```
		{
		  "success": true
		}
		```

- PATCH '/actors/<int:id>'
	- Updtae Actor info and insert it db
	- Request Argument : `Actor id`  `name` `email` `age` `salary` 
	- Returns : JSON response containing request status
	- example
		```
		{
		  "success": true
		}
		```

- PATCH '/movies/<int:id>'
	- Updtae Movie info and insert it db
	- Request Argument : `Movie id` `name` `length` `genre`
	- Returns : JSON response containing request status
	- example
		```
		{
		  "success": true
		}
		```

- DELETE '/actors/<int:id>'
	- Delete Actor from db
	- Request Argument : Actor id
	- Returns : JSON response containing request status
	- example
		```
		{
		  "success": true
		}
		```

- DELETE '/movies/<int:id>'
	- Delete Movie from db
	- Request Argument : Movie id
	- Returns : JSON response containing request status
	- example
		```
		{
		  "success": true
		}
		```


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for the platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

After setting up the virtual environment, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

**Note: If you add any other library to this project, remember to always run the command below to update your requirements.txt file*
```bash
pip freeze > requirements.txt
```


## Running the server

first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app/__init__.py` directs flask to use the this file to find the application.

## Authentication

Tokens nand jwts needed for Authentivation can be found in the `setup.sh` file

## API Reference

### Getting Started

- Base URL: You can run this API locally at the default `http://127.0.0.1:5000/`
- Authentication: This app has 3 users. Each has his own token which are provided in `setup.sh` file. Details about each user privlages are provided below.



### Users

This app has 3 users. each user has his own privileges.

- Casting Assistant
	- Can view actors and movies

- Casting Director
	- All permissions a Casting Assistant has and…
	- Add or delete an actor from the database
	- Modify actors or movies

- Executive Producer
	- All permissions a Casting Director has and…
	- Add or delete a movie from the database

Please Note, to use any endpoint, you must send the request with user access token in Authorization header, which are provided in `setup.sh`.


## Testing

To run the tests, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < db.psql
source setup.sh
python test_app.py
```
## Author
Adenle Abiodun  `adenleabbey@hotmail.com`