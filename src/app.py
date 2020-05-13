from flask import Flask, jsonify
from src.database.models import setup_db
from flask_cors import CORS
import psycopg2

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)