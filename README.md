# CAPSTONE

## Summary

This project provides an API backend for a casting agency management application - containing up to this version - CRUD actions for movies and actors

Live at ['heroku app'](https://dev-leticia-casting-agency.herokuapp.com)

### Installing Dependencies

navigate to  root `/` directory and run:

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from a potential frontend server. 

## Database Setup
With Postgres running, initialize the the database
```bash
createdb <db_name>
```

## Running the server

First update db_path variable under `/src/database/models` with your database URL and port(if applicable).

Then from the `/` directory first ensure you are using a virtual environment then to run the server, execute:

Export necessary environment variables:
```bash
export DB_PATH=postgres://user:password@localhost:5432/<db_name>
export FLASK_APP=app.py
```

Run flask app
```bash
flask run --reload
```

## Running tests

For turning on/off a pre-setup test database environment uncomment function call `restart_db_with_test_data()` on `models.py`
and run the script below:

```bash
python test_app.py
```

## Authentication and Testing

Authentication was implemented with JWT token validation following a role/permission based authentication schema.
The `postman_collection.json` located in `/` contains a Postman test collection with updated tokens within request headers for each role setup in Auth0.
The collection header variable `HOST` is setup to make requests to a live version on the app hosted on Heroku (https://dev-leticia-casting-agency.herokuapp.com/
) feel free to change the variable value to your `localhost:port` and run the tests on your database.

### User Roles

#### Casting Assistant

A casting assistant can view actors and movies

#### Casting Director

A casting director extends the permissions of the casting assistant by adding and deleting actors from the database. They can also modify actors and movies

#### Executive Producer

The executive producer extends the permissions of the casting director by adding or deleting movies from the database

## API Endpoints - Actors

- GET '/actors'
- GET '/actors/{actor_id}'
- POST '/actors'
- PATCH '/actors/{actor_id}'
- DELETE '/actors/{actor_id}'

-----

GET '/actors'
- Fetches actors from the database with name, gender and age
- Request Arguments: None
- Returns: An object with a list of actors and their information
```
{
  "actors": [
    {
      "age": 55,
      "gender": "non-binary",
      "id": 1,
      "name": "Sarah Jessica Tester"
    }
  ],
  "success": true
}
```

GET '/actors/{actor_id}'
- Fetches an actor information from the database where actor_id exists
- Request Arguments: None
- Returns: An object with an actor's information
```
{
  "actor": {
      "age": 55,
      "gender": "non-binary",
      "id": 1,
      "name": "Sarah Jessica Tester"
    }
  "success": true
}
```

POST '/actors'
- Add an actor to the database
- Request body parameter: JSON Object with age as an integer, gender as a string, name as a string
- Returns: An object with an actor's information
Example payload:
```
{     
    "age": 55,
    "gender": "non-binary",
    "name": "Sarah Jessica Tester"
}
```

PATCH '/actors/{actor_id}'
- Edit an actors information in the database
- Path argument: Actor id as a integer
- Request body parameters: 
JSON Object containing one or all age as integer, gender as a string, name as a string
Example payload:
```
{
    "gender": "Female"
}
```
- Returns: An object with an actor's information

DELETE '/actors/{actor_id}'
- delete an actor in the database
- Path argument: Actor id as a integer
- Returns: deleted actor id
```
{
    "deleted_actor_id": 1
}
```

## API Endpoints - Movies

- GET '/movies'
- GET '/movies/{movie_id}'
- POST '/movies'
- PATCH '/movies/{movie_id}'
- DELETE '/movies/{movie_id}'

-----

GET '/movies'
- Fetches a list of movies from the database
- Request Arguments: None
- Returns: An object with a list of movies and their information
```
{
  "movies": [
    {     
        "id": 1
        "title": "Pretty Woman",
        "release_date": "1989-12-11"
    },
    {     
        "id": 14
        "title": "Pretty Woman II",
        "release_date": "1995-09-01"
    }
  ],
  "success": true
}
```

GET '/movies/{movie_id}'
- Fetches a movie's information from the database where movie id exists
- Request Arguments: None
- Returns: An object with a movie's information
```
{
  "movie": {     
        "id": 1
        "title": "Pretty Woman",
        "release_date": "1989-12-11"
    }
  "success": true
}
```

POST '/movies'
- Add a movie to the database
- Request body parameter: JSON Object containing title as string and date_released as a date
- Returns: An object with a movie's information
Example payload:
```
{     
    "title": "Pretty Woman",
    "release_date": "1989-12-11"
}
```

PATCH '/movies/{movie_id}'
- Edit a movie information in the database
- Path argument: movie id as a integer
- Request body parameters: 
JSON Object containing one or both title as string, date_released as a date
Example payload:
```
{
    "title": "Pretty Woman"
}
```
- Returns: An object with an movie's information

DELETE '/movies/{movie_id}'
- delete a movie in the database
- Path argument: movie id as a integer
- Returns: deleted movie id
```
{
    "deleted_movie_id": 1
}
```