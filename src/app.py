from flask import Flask, jsonify, request, abort
from src.database.models import setup_db, Actor, Movie
from flask_cors import CORS

def create_app(test_config=None):
    app_ = Flask(__name__)
    CORS(app_)
    return app_


app = create_app()
setup_db(app)

@app.route('/')
def index():
    return jsonify({
        'message': 'success'
    })

@app.route('/actors')
def get_actors():
    # query all actors from table
    raw_actors = Actor.query.all()
    # extract information from actors using its format() method
    actors = [actor.format() for actor in raw_actors]
    # checks for presence of results in actors list
    if not len(actors):
        abort(404)

    return jsonify({
        'success': True,
        'actors': actors
    })

@app.route('/actor/<int:id>')
def get_actor(id):
    # query all actor with matching id as the param
    actor = Actor.query.filter_by(id=id).one_or_none()
    # checks for presence of a result
    if not actor:
        abort(404)

    return jsonify({
        'success': True,
        'actor': actor.format()
    })

@app.route('/actors', methods=['POST'])
def create_actor():
    data = request.get_json()
    # checks for presence of results in actors list
    if not data:
        abort(400)

    # retrieves data from request
    name = data['name']
    age = data['age']
    gender = data['gender']
    # creates a new instance of actor passing the retrieved data
    actor = Actor(name=name, age=age, gender=gender)
    try:
        actor.insert()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'actor': actor.format()
    })

@app.route('/actor/<int:id>/edit', methods=['PATCH'])
def edit_actor(id):
    actor = Actor.query.filter_by(id=id).one_or_none()
    # check for existence of actor in db
    if not actor:
        abort(404)

    data = request.get_json()
    # checks for presence of data in request
    if not data:
        abort(400)

    # in case new value for attribute was present in request
    if 'name' in data:
        actor.name = data['name']
    if 'age' in data:
        actor.age = data['age']
    if 'gender' in data:
        actor.age = data['gender']

    try:
        actor.update()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'actor': actor.format()
    })

@app.route('/actor/<int:id>', methods=['DELETE'])
def delete_actor(id):
    # query all actor with matching id as the param
    actor = Actor.query.filter_by(id=id).one_or_none()
    # checks for presence of a result
    if not actor:
        abort(404)
    # delete actor from database
    try:
        actor.delete()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'deleted_actor_id': id
    })



'''                 
    ERROR HANDLERS
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)