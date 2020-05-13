from flask import Flask, jsonify
from src.database.models import setup_db

app = Flask(__name__)
setup_db(app)

@app.route('/')
def index():
    return jsonify({
        'message': 'success'
    })
