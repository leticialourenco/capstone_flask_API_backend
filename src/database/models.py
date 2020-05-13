from flask_sqlalchemy import SQLAlchemy

db_path = 'postgres://leticia:5678@localhost:5432/MOCK'
db = SQLAlchemy()

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
